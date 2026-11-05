---
name: agyos-binary-analysis
description: Static and dynamic reverse engineering of binaries, compiled applications, and network protocols. Bridges disassembly engines, decompilation validation, and runtime tracing within AGYOS.
---

# AGYOS Binary Analysis & Reverse Engineering

An operational guide for inspecting compiled executables, understanding binary architectures, and reverse-engineering proprietary network protocols for security research and interoperability.

## 1. Supported Executable Formats

The analysis pipeline supports native and bytecode targets:
- Native Binaries: ELF (Linux), Mach-O (macOS/iOS), PE32/PE32+ (Windows).
- Virtual Machine Bytecode: JVM `.class`/`.jar`, .NET CLR assemblies, Dalvik/ART (`.dex`/`.apk`), WebAssembly (`.wasm`).

## 2. Core Toolchain & Environments

- Disassembly & Decompilation: Ghidra (headless scripting), radare2 / rizin (`r2pipe`), Hopper Disassembler, IDA Free.
- Binary Inspection: `readelf`, `objdump`, `nm`, `strings`, `binwalk`, `checksec`.
- Dynamic Tracing: Frida (cross-platform JavaScript instrumentation), `strace`, `ltrace`, GDB with GEF/PEDA.
- Network Protocol Interception: Wireshark / tshark, mitmproxy (TLS interception).

## 3. Static Analysis Protocol

Execute static inspection sequentially before running dynamic processes:

1. Metadata & Hardening Audit:
   ```bash
   file target_binary
   checksec --file=target_binary
   ```
   - Identify architecture (x86_64, ARM64), linking (static vs dynamic), and security mitigations (PIE, stack canaries, NX/DEP, RELRO).

2. String & Symbol Extraction:
   - Filter readable ASCII/UTF-16 strings with length thresholds:
     ```bash
     strings -n 8 target_binary | grep -E "https?://|/api/|key|token|auth"
     ```
   - Export exported/imported symbols via `nm -D` or `readelf -s`.

3. Decompilation & Control Flow Recovery:
   - Identify main entry points, dispatch tables, and cryptographic primitives.
   - Trace cross-references (`xrefs`) to sensitive APIs (socket operations, filesystem writes, crypto keys).

## 4. Dynamic Runtime Tracing

1. System Call Tracing:
   ```bash
   strace -f -e trace=network,file -s 256 ./target_binary
   ```
   - Pinpoints file descriptors, socket connections, and configuration file lookups.

2. Function Hooking with Frida:
   ```javascript
   // hook_crypto.js
   Interceptor.attach(Module.findExportByName(null, "EVP_EncryptInit_ex"), {
     onEnter: function (args) {
       console.log("[+] Cipher context initialized: " + args[1]);
     }
   });
   ```
   - Attach via: `frida -l hook_crypto.js -f ./target_binary`

## 5. Protocol Reverse Engineering

When reconstructing undocumented network protocols:
- Capture raw PCAP streams under controlled baseline workloads.
- Segment payloads into framing headers (magic bytes, length delimiters, message type IDs) and payload bodies.
- Test decoding hypotheses with schema definitions (Protobuf, MessagePack, or custom binary structs).
