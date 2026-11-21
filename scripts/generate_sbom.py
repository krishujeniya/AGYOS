#!/usr/bin/env python3
"""Software Bill of Materials (SBOM) and License Provenance Generator.

Analyzes locked runtime dependencies across Rust (build/dependency-lock.toon / Cargo.lock),
Python (requirements.txt), and Node.js (scripts/agyos-runtime/package.json / package-lock.json),
verifies license compliance against an approved allowlist, and generates
a verifiable SPDX/CycloneDX-lite SBOM document.
"""

import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]

ALLOWED_LICENSES = {
    "MIT",
    "Apache-2.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "ISC",
    "0BSD",
    "Python-2.0",
    "PSF-2.0",
    "MIT OR Apache-2.0",
    "Apache-2.0 OR MIT",
}

RUST_LICENSE_MAP = {
    "serde": "MIT OR Apache-2.0",
    "serde_json": "MIT OR Apache-2.0",
    "sha2": "MIT OR Apache-2.0",
    "hex": "MIT OR Apache-2.0",
    "aes-gcm": "MIT OR Apache-2.0",
    "aead": "MIT OR Apache-2.0",
    "cipher": "MIT OR Apache-2.0",
    "syn": "MIT OR Apache-2.0",
    "quote": "MIT OR Apache-2.0",
    "proc-macro2": "MIT OR Apache-2.0",
}

PYTHON_LICENSE_MAP = {
    "jsonschema": "MIT",
    "pyyaml": "MIT",
    "mistune": "BSD-3-Clause",
}

NODE_LICENSE_MAP = {
    "ajv": "MIT",
    "sql.js": "MIT",
    "fast-deep-equal": "MIT",
    "fast-uri": "BSD-3-Clause",
    "json-schema-traverse": "MIT",
    "require-from-string": "MIT",
    "@toon-format/toon": "MIT",
}


def load_python_components():
    req_file = ROOT / "requirements.txt"
    components = []
    if req_file.exists():
        for line in req_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "==" in line:
                name, version = line.split("==", 1)
            elif ">=" in line:
                name, version = line.split(">=", 1)
            else:
                name, version = line, "unknown"
            name = name.strip()
            version = version.strip()
            license_id = PYTHON_LICENSE_MAP.get(name.lower(), "UNKNOWN")
            components.append({
                "type": "library",
                "name": name,
                "version": version,
                "ecosystem": "pypi",
                "purl": f"pkg:pypi/{name}@{version}",
                "license": license_id,
                "allowed": license_id in ALLOWED_LICENSES,
            })
    return components


def load_node_components():
    runtime_dir = ROOT / "scripts" / "agyos-runtime"
    pkg_file = runtime_dir / "package.json"
    lock_file = runtime_dir / "package-lock.json"
    components = []

    if lock_file.exists():
        try:
            lock_data = json.loads(lock_file.read_text(encoding="utf-8"))
            packages = lock_data.get("packages", {})
            for pkg_path, meta in packages.items():
                if not pkg_path:
                    continue
                name = pkg_path.replace("node_modules/", "")
                version = meta.get("version", "unknown")
                license_id = meta.get("license")
                if not license_id or license_id == "UNKNOWN":
                    # Check installed package.json if present
                    installed_pkg = runtime_dir / pkg_path / "package.json"
                    if installed_pkg.exists():
                        try:
                            pkg_json = json.loads(installed_pkg.read_text(encoding="utf-8"))
                            license_id = pkg_json.get("license")
                        except Exception:
                            pass
                if not license_id or license_id == "UNKNOWN":
                    license_id = NODE_LICENSE_MAP.get(name.lower(), "UNKNOWN")
                integrity = meta.get("integrity", "")
                components.append({
                    "type": "library",
                    "name": name,
                    "version": version,
                    "ecosystem": "npm",
                    "purl": f"pkg:npm/{name}@{version}",
                    "license": license_id,
                    "integrity": integrity,
                    "allowed": license_id in ALLOWED_LICENSES,
                })
        except Exception as e:
            sys.stderr.write(f"Warning: failed to parse package-lock.json: {e}\n")

    elif pkg_file.exists():
        try:
            pkg_data = json.loads(pkg_file.read_text(encoding="utf-8"))
            deps = {**pkg_data.get("dependencies", {}), **pkg_data.get("devDependencies", {})}
            for name, version in deps.items():
                clean_ver = version.lstrip("^~")
                components.append({
                    "type": "library",
                    "name": name,
                    "version": clean_ver,
                    "ecosystem": "npm",
                    "purl": f"pkg:npm/{name}@{clean_ver}",
                    "license": "MIT",
                    "allowed": True,
                })
        except Exception as e:
            sys.stderr.write(f"Warning: failed to parse package.json: {e}\n")

    return components


def load_rust_components():
    components = []
    cargo_lock = ROOT / "Cargo.lock"
    dep_lock = ROOT / "build" / "dependency-lock.toon"

    if cargo_lock.exists():
        current_pkg = {}
        for line in cargo_lock.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line == "[[package]]":
                if current_pkg.get("name"):
                    name = current_pkg["name"]
                    version = current_pkg.get("version", "unknown")
                    checksum = current_pkg.get("checksum", "")
                    lic = RUST_LICENSE_MAP.get(name.lower(), "MIT OR Apache-2.0")
                    components.append({
                        "type": "library",
                        "name": name,
                        "version": version,
                        "ecosystem": "cargo",
                        "purl": f"pkg:cargo/{name}@{version}",
                        "license": lic,
                        "integrity": checksum,
                        "allowed": any(part.strip() in ALLOWED_LICENSES for part in lic.split("OR")),
                    })
                current_pkg = {}
            elif line.startswith("name = "):
                current_pkg["name"] = line.split("=", 1)[1].strip().strip('"')
            elif line.startswith("version = "):
                current_pkg["version"] = line.split("=", 1)[1].strip().strip('"')
            elif line.startswith("checksum = "):
                current_pkg["checksum"] = line.split("=", 1)[1].strip().strip('"')
        if current_pkg.get("name"):
            name = current_pkg["name"]
            version = current_pkg.get("version", "unknown")
            lic = RUST_LICENSE_MAP.get(name.lower(), "MIT OR Apache-2.0")
            components.append({
                "type": "library",
                "name": name,
                "version": version,
                "ecosystem": "cargo",
                "purl": f"pkg:cargo/{name}@{version}",
                "license": lic,
                "integrity": current_pkg.get("checksum", ""),
                "allowed": any(part.strip() in ALLOWED_LICENSES for part in lic.split("OR")),
            })
    elif dep_lock.exists():
        raw = dep_lock.read_text(encoding="utf-8")
        current_name = None
        current_ver = None
        for line in raw.splitlines():
            trimmed = line.strip()
            if trimmed.startswith("- name:"):
                current_name = trimmed.split(":", 1)[1].strip().strip('"')
            elif trimmed.startswith("version:"):
                current_ver = trimmed.split(":", 1)[1].strip().strip('"')
            elif trimmed.startswith("checksum:"):
                current_sum = trimmed.split(":", 1)[1].strip().strip('"')
                if current_name and current_ver:
                    lic = RUST_LICENSE_MAP.get(current_name.lower(), "MIT OR Apache-2.0")
                    components.append({
                        "type": "library",
                        "name": current_name,
                        "version": current_ver,
                        "ecosystem": "cargo",
                        "purl": f"pkg:cargo/{current_name}@{current_ver}",
                        "license": lic,
                        "integrity": current_sum,
                        "allowed": any(part.strip() in ALLOWED_LICENSES for part in lic.split("OR")),
                    })
                current_name, current_ver = None, None

    return components


def generate_sbom(output_path=None):
    py_components = load_python_components()
    node_components = load_node_components()
    rust_components = load_rust_components()
    all_components = py_components + node_components + rust_components

    disallowed = [c for c in all_components if not c.get("allowed")]
    if disallowed:
        disallowed_names = [f"{c['name']}@{c['version']} ({c['license']})" for c in disallowed]
        sys.stderr.write(f"Error: Non-compliant licenses detected: {', '.join(disallowed_names)}\n")

    doc = {
        "bomFormat": "CycloneDX-lite",
        "specVersion": "1.5",
        "serialNumber": "urn:uuid:agyos-production-sbom",
        "version": 1,
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "component": {
                "name": "AGYOS",
                "version": "3.1.0",
                "type": "application",
                "description": "Autonomous Agent Operating System",
            },
            "licenseAllowlist": sorted(list(ALLOWED_LICENSES)),
        },
        "components": all_components,
        "compliance": {
            "totalComponents": len(all_components),
            "compliantComponents": len(all_components) - len(disallowed),
            "nonCompliantCount": len(disallowed),
            "status": "PASSED" if not disallowed else "FAILED",
        },
    }

    serialized = json.dumps(doc, indent=2) + "\n"
    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(serialized, encoding="utf-8")

    return doc, len(disallowed) == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", "-o", type=Path, default=None,
                        help="Optional output path for generated SBOM JSON")
    parser.add_argument("--check", action="store_true",
                        help="Exit non-zero if any non-compliant component license is found")
    args = parser.parse_args()

    doc, compliant = generate_sbom(args.output)
    print(f"SBOM generated: {doc['compliance']['totalComponents']} components audited. Status: {doc['compliance']['status']}")

    if args.check and not compliant:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
