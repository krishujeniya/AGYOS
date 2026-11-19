---
name: jake-console-console-reverse
description: "Reverse Engineer. Opens your own disc image, finds the game's code and maps how it works: the boot ELF, every function, the design doc. Drives the whole port and is the entry point of the Console pack. Reads ISO 9660 images without loading them whole, reads SYSTEM.CNF and the boot ELF (segments, CRC-32 and PCSX2 CRC, IRX modules), writes a starter PS2Recomp TOML with real keys only, and keeps console/STATE.md, the memory every /console-* skill reads first. Carries the PS2Recomp rules: never clean the build, never edit generated code or headers, a build gate, and a three-strike circuit breaker. Use when the user says \"port my PS2 game\", \"recompile my game\", \"open my ISO\", \"what's on this disc\", \"set up PS2Recomp\", \"where are we\", \"continue the port\", or at the start of any Console session."
license: MIT
metadata:
  upstream_repository: Jakeschincariol/console-skill
  upstream_skill: console-reverse
  upstream_commit: a508929f1e8f5dd6f54afe489fd74340df3b6f74
prompt-source: prompt.toon
---
skill: "jake-console-console-reverse"
status: unavailable
instruction: This entry has no operational instructions or tools. Refer defensive findings to the owner within written scope.
