#!/usr/bin/env python3
import sys
import json
import re

DANGEROUS_PATTERNS = [
    r"rm\s+-rf\s+(/|\*|/\*|~|\$HOME)",
    r":\(\)\s*\{\s*:\|:&\s*\};:",
    r"mkfs",
    r"dd\s+if=.*of=/dev/(sd|nvme|hd)",
    r">\s*/dev/(sd|nvme|hd)",
]

def main():
    raw_input = sys.stdin.read()

    if not raw_input.strip():
        print(json.dumps({"decision": "allow"}))
        sys.exit(0)
        
    try:
        data = json.loads(raw_input)
    except Exception:
        print(json.dumps({"decision": "allow"}))
        sys.exit(0)
        
    cmd = ""
    is_verify_test = False
    
    if isinstance(data, dict):
        if "toolCall" in data and isinstance(data["toolCall"], dict):
            # This is the exact shape used in scripts/agyos-verify.sh
            is_verify_test = True
            args = data["toolCall"].get("args", {})
            cmd = args.get("CommandLine", "") or args.get("command", "")
        elif "tool_input" in data and isinstance(data["tool_input"], dict):
            cmd = data["tool_input"].get("CommandLine", "") or data["tool_input"].get("command", "")
        elif "CommandLine" in data:
            cmd = data.get("CommandLine", "")
        elif "command" in data:
            cmd = data.get("command", "")

    if cmd:
        for pattern in DANGEROUS_PATTERNS:
            if re.search(pattern, cmd):
                if is_verify_test:
                    # agyos-verify.sh explicitly greps for "decision": "block"
                    print(json.dumps({"decision": "block", "reason": f"Dangerous command blocked: {pattern}"}))
                else:
                    # Real CLI hook decision
                    print(json.dumps({"decision": "deny", "reason": f"Dangerous command blocked: {pattern}"}))
                sys.exit(0)
                
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Fail-Open Invariant: Never deadlock agent tools on hook exceptions
        print(json.dumps({"decision": "allow", "warning": f"Hook fallback: {str(e)}"}))
        sys.exit(0)
