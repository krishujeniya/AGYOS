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

def command_from_payload(data):
    if not isinstance(data, dict):
        return ""
    tool_call = data.get("toolCall")
    if isinstance(tool_call, dict):
        args = tool_call.get("args", {})
    else:
        args = data.get("tool_input", data)
    if not isinstance(args, dict):
        return ""
    cmd = args.get("CommandLine") or args.get("command", "")
    return cmd if isinstance(cmd, str) else ""


def main(event):
    # Only PreToolUse accepts a permission decision. Other events are no-ops.
    if event != "PreToolUse":
        print(json.dumps({"decision": "allow"} if event == "Stop" else {}))
        return

    raw = sys.stdin.read(1048577)
    if len(raw) > 1048576:
        print(json.dumps({"decision": "deny", "reason": "Hook event too large"}))
        return
    try:
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError("Expected event object")
        args = data.get("toolCall", {}).get("args", {}) if isinstance(data.get("toolCall"), dict) else data.get("tool_input", data)
        if not isinstance(args, dict):
            raise ValueError("Invalid tool arguments")
        candidate = args.get("CommandLine", args.get("command", ""))
        if not isinstance(candidate, str):
            raise ValueError("Command must be text")
    except (ValueError, UnicodeError, TypeError):
        print(json.dumps({"decision": "deny", "reason": "Invalid tool event (fail closed)"}))
        return
    cmd = command_from_payload(data)
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, cmd):
            print(json.dumps({"decision": "deny", "reason": f"Dangerous command blocked: {pattern}"}))
            return
    print(json.dumps({"decision": "allow"}))

if __name__ == "__main__":
    event = sys.argv[1] if len(sys.argv) > 1 else "PreToolUse"
    try:
        main(event)
    except Exception as e:
        # Keep diagnostics out of the event's JSON response.
        print(f"Hook fallback: {e}", file=sys.stderr)
        print(json.dumps({"decision": "deny", "reason": "Hook failed closed"} if event == "PreToolUse" else ({"decision": "allow"} if event == "Stop" else {})))
