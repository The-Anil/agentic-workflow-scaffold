# CLAUDE.md

<!-- AUTO-MANAGED: Claude maintains this file. Do not edit manually. -->
<!-- Status: UNINITIALIZED -->

## Setup status
This project has not been initialized yet.

On your very first message — regardless of what the user says — read `.claude/skills/bootstrap/SKILL.md` and run the bootstrap process before doing anything else. Even if the user gives a feature request, bootstrap first, then handle the request.

---

## Scratch mode

To start a session that is NOT part of the project — analysis, exploration, throwaway scripts, reviewing files — say:

> "scratch mode" or "this is not a project session"

In scratch mode:
- Bootstrap does NOT run
- CONTEXT.md is NOT updated
- MEMORY.md is NOT written
- session-handoff skill does NOT trigger
- All hooks still run (security guardrails stay on)

To exit scratch mode and return to normal project sessions, start a new Claude Code session normally.
