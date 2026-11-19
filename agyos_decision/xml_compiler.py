"""AGYOS XML Semantic Compiler (Deprecated Shim).

This module is retained for backward compatibility.
All compilation now routes through the pure TOON compiler (toon_compiler.py).
"""

from __future__ import annotations

from .toon_compiler import (
    prune_conversational_filler,
    minify_toon,
    minify_xml,
    compile_skill_to_toon,
    compile_skill_to_xml,
    compile_agent_to_toon,
    compile_agent_to_xml,
    compile_task_to_toon,
    compile_task_to_xml,
    compile_cached_toon_prompt,
    compile_cached_prompt,
)

__all__ = [
    "prune_conversational_filler",
    "minify_toon",
    "minify_xml",
    "compile_skill_to_toon",
    "compile_skill_to_xml",
    "compile_agent_to_toon",
    "compile_agent_to_xml",
    "compile_task_to_toon",
    "compile_task_to_xml",
    "compile_cached_toon_prompt",
    "compile_cached_prompt",
]
