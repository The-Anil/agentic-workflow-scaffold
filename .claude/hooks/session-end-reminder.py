#!/usr/bin/env python3
"""
Hook: session-end-reminder
Event: Stop
Reminds Claude to run the session-handoff skill before the session closes.
Does NOT fire in scratch mode (when CLAUDE.md contains SCRATCH_MODE).
"""
import sys
import json
from pathlib import Path

# Skip reminder in scratch mode
claude_md = Path("CLAUDE.md")
if claude_md.exists() and "SCRATCH_MODE" in claude_md.read_text(encoding="utf-8"):
    sys.exit(0)

print(json.dumps({
    "systemMessage": (
        "Session ending. If any work was done this session, "
        "trigger the session-handoff skill now to rewrite CONTEXT.md "
        "and capture decisions in MEMORY.md before closing."
    )
}))

sys.exit(0)
