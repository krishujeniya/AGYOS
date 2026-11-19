"""Materialize the catalog cutover in GitHub Actions for review as a patch."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agyos_decision.catalog import read_metadata
from agyos_decision.skill_prompts import migrate_skill


def main():
    for manifest in sorted((ROOT / ".agents/skills").rglob("SKILL.md")):
        if "prompt-source" in read_metadata(manifest):
            continue
        host, source = migrate_skill(manifest, manifest.read_text(encoding="utf-8"))
        manifest.with_name("prompt.toon").write_text(source, encoding="utf-8")
        manifest.write_text(host, encoding="utf-8")


if __name__ == "__main__":
    main()
