---
trigger: glob
globs: "**/*.py,**/*.pyi"
---
# Python Coding Style

> This file extends [common/coding-style.md](common-coding-style.md) with Python specific content.

## Standards

- Follow **PEP 8** conventions
- Use **type annotations** on all function signatures

## Immutability

Prefer immutable data structures:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    name: str
    email: str

from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float
```

## Formatting

- **black** for code formatting
- **isort** for import sorting
- **ruff** for linting

## Tooling & Package Management

- **Mandatory UV Exclusively**: ALWAYS use `uv` for all Python operations, dependency management, virtual environments, scripts, and tooling (`uv run`, `uv pip`, `uv venv`, `uv add`, `uv tool`, `uvx`).
- **Zero Python/Pip Without UV**: NEVER invoke raw `python`, `python3`, `pip`, `pip3`, or `virtualenv` directly without `uv`.
- **Standards**: Enforce `pyproject.toml` and `uv.lock` for deterministic dependency trees.

## Reference

See skill: `python-patterns` for comprehensive Python idioms and patterns.
