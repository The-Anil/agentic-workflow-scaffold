#!/usr/bin/env python3
"""
Hook: no-git-add-dot
Event: PreToolUse (Bash)
Blocks git add . / git add -A / git add --all.
Forces surgical staging — only specific files.
Exit 2 = blocked.
"""
import sys
import json

data = json.load(sys.stdin)
cmd = data.get("tool_input", {}).get("command", "")

BLOCKED = [
    "git add .",
    "git add -A",
    "git add --all",
    "git add -a",
]

if any(blocked in cmd for blocked in BLOCKED):
    print(json.dumps({
        "reason": (
            "Blocked: 'git add .' and 'git add -A' are not allowed. "
            "Stage files surgically: 'git add <specific-file>'. "
            "This ensures only task-related files are committed."
        )
    }))
    sys.exit(2)

sys.exit(0)
