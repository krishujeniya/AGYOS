import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read_toon_skill(directory: Path) -> str:
    header_raw = (directory / "SKILL.toon").read_text(encoding="utf-8")
    m = re.search(r'^header: ("(?:[^"\\]|\\.)*")', header_raw, re.M)
    assert m, f"Missing header in {directory / 'SKILL.toon'}"
    header = json.loads(m.group(1))
    prompt = (directory / "prompt.toon").read_text(encoding="utf-8")
    return header + prompt


def test_skill_files_exist_and_are_identical():
    root_toon = ROOT / "SKILL.toon"
    copy_toon = ROOT / "skills" / "chopify" / "SKILL.toon"
    root_prompt = ROOT / "prompt.toon"
    copy_prompt = ROOT / "skills" / "chopify" / "prompt.toon"
    assert root_toon.exists() and copy_toon.exists()
    assert root_prompt.exists() and copy_prompt.exists()
    assert root_toon.read_text(encoding="utf-8") == copy_toon.read_text(encoding="utf-8")
    assert root_prompt.read_text(encoding="utf-8") == copy_prompt.read_text(encoding="utf-8")


def test_skill_has_frontmatter_and_workflow():
    text = _read_toon_skill(ROOT)
    assert text.startswith("---\n")
    assert "name: chopify" in text
    assert "description:" in text
    assert "project.create" in text
    assert "project.prepare" in text
    assert "project.get" in text
    assert "project.render" in text
    assert "project.wait" in text


def test_skill_operation_names_are_in_catalog():
    proc = subprocess.run([sys.executable, "agent.py", "describe"],
                          cwd=ROOT, capture_output=True, text=True)
    catalog = json.loads(proc.stdout.strip().splitlines()[-1])["data"]
    names = {op["name"] for op in catalog["operations"]}
    text = _read_toon_skill(ROOT)
    mentioned = set(re.findall(
        r"\b(?:project|batch|live|preflight|styles|describe)\.[a-z.]+"
        r"|\b(?:describe|preflight|styles)\b", text))
    assert mentioned <= names | {"describe", "preflight", "styles"}
