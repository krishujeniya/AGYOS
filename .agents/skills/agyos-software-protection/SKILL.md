---
name: agyos-software-protection
description: Defensive software hardening and counter-reverse-engineering playbook. Protects proprietary binaries and builds against automated AI decompilation, resource exhaustion, and static pattern mining.
---

# AGYOS Software Protection & Anti-Decompilation

A defensive engineering guide for hardening shipped binaries and client applications against automated reverse engineering, automated AI agent analysis, and unauthorized static extraction.

## 1. Defensive Threat Model

When shipping client-side software, automated analysis agents and reverse engineers attempt to:
- Extract private API schemas, cryptographic routines, and proprietary algorithms.
- Run automated decompilers to reconstruct full source trees.
- Trace execution flow to bypass client-side license checks or telemetry.

The defense objective is to dramatically increase the computational, token, and reasoning budget required to analyze the binary while maintaining deterministic runtime performance for legitimate users.

## 2. Binary Stripping & Symbol Sanitization

1. Symbol Table Removal:
   - Strip debug symbols, source file paths, and local symbol tables prior to distribution:
     ```bash
     strip --strip-all target_binary
     ```
2. Compiler Flag Hardening:
   - Compile release builds with optimization and security flags:
     ```bash
     CFLAGS="-O3 -fvisibility=hidden -fstack-protector-strong -D_FORTIFY_SOURCE=2 -Wl,-z,relro,-z,now"
     ```

## 3. Control-Flow Flattening & Opaque Predicates

1. Control-Flow Flattening:
   - Break linear basic blocks into discrete case statements controlled by an internal state variable dispatched within an infinite loop.
   - Effect: Prevents automated AI decompilation engines from reconstructing structured `if/else` and `while` loops.

2. Opaque Predicates:
   - Introduce branch conditionals that evaluate to a constant boolean value at runtime based on mathematical invariants (e.g., $x^2 \ge 0$), but cannot be proven constant by static AST analyzers.

## 4. String & Constant Encryption

- Never store sensitive strings (API endpoints, error messages, configuration keys) as plaintext ASCII/UTF-8 literals in `.rodata`.
- Encrypt strings at compile time using XOR or AES with localized keys.
- Decrypt into temporary buffers on the stack immediately before use, and zeroize memory (`memset_s` / `explicit_bzero`) upon completion.

## 5. Decoy Pathways & Analysis-Resource Exhaustion

- Inject plausible decoy functions resembling cryptographic or license-verification routines.
- Force automated AI analysis agents to traverse complex, dead-end call graphs that exhaust model context windows and execution token budgets.
- Ensure all decoy code is isolated from core execution paths so application performance remains unaffected.

## 6. Runtime Integrity & Anti-Instrumentation

- Detect Debugger Attachment: Monitor `ptrace` status on Linux (`/proc/self/status` `TracerPid`) or `sysctl` `P_TRACED` on macOS.
- Hook Detection: Validate function prologues of critical system APIs to identify Frida trampolines or dynamic inline patches.
- Binary Checksums: Verify executable text segment hashes at startup to detect binary tampering or memory patching.
