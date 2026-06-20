---
description: Initialize a new project. Triggers automatically when CLAUDE.md contains "UNINITIALIZED". Runs before anything else on first project session. Does NOT run in scratch mode.
---

# Bootstrap

## When to trigger
- CLAUDE.md contains the word "UNINITIALIZED" AND the user has not invoked scratch mode
- User explicitly says "set up this project", "initialize", "bootstrap"

## When NOT to trigger
- User says "scratch mode", "this is not a project session", "just analyzing", "exploration only"
- In these cases: acknowledge scratch mode, skip all bootstrap steps, skip CONTEXT.md and MEMORY.md, proceed to help with what was asked

---

## Scratch mode response

If the user invokes scratch mode, reply with exactly:

```
Scratch mode active. I won't bootstrap, update CONTEXT.md, or write to memory this session.
Hooks (secret-block, prod-guard, etc.) are still active.
What do you want to explore?
```

Then help with whatever they asked. Do not touch CLAUDE.md, CONTEXT.md, or MEMORY.md.

---

## Step 1 — gather context in one message

Ask all of the following at once. Never ask one at a time:

```
Before we start building, I need a few details to set up your project correctly.

1. What does this project do? (one paragraph)
2. What is the tech stack? (languages, frameworks, key libraries)
3. What commands run the project? (dev server, tests, lint, build)
4. Do you have a preferred folder structure, or should I propose one based on the stack?
5. Any hard rules I should always follow? (e.g. "never use classes", "always validate inputs at the boundary")
6. What should I never do without asking you first?
```

Wait for all answers before proceeding.

---

## Step 2 — propose structure and conventions

Based on the answers, show:
- Folder layout as a tree
- Naming conventions
- Key architectural boundaries

```
Here's the structure I'll use. Tell me what to change before I lock it in.

[folder tree]
[naming conventions]
[key architectural rules]

Approve this, or tell me what to change.
```

Wait for explicit approval. Do not write any files until approved.

---

## Step 3 — write CLAUDE.md

Replace the entire contents of `CLAUDE.md` with the template below, filled with real project details.

```markdown
# CLAUDE.md

<!-- AUTO-MANAGED: Claude maintains this file. Do not edit manually unless correcting an error. -->
<!-- Initialized: [YYYY-MM-DD] -->

## Project
[Name - one line]
[Description - one paragraph]

## Stack
[Each framework/library on its own line]

## Commands
[Exact commands - dev server, test, lint, build, type-check]

## Project structure
[The approved folder tree - exact paths]

## Naming conventions
[Derived from stack and user preferences]

## Architectural rules
[Key boundaries that must not be crossed]

## Code rules
- Write the minimum code needed. No unrequested features or abstractions.
- Surgical edits only - change exactly the lines needed, leave adjacent code untouched.
- Match the existing file style (naming, spacing, import order).
- Never introduce a new dependency without flagging it and getting approval.
- State assumptions explicitly before writing code.
- Stop and ask on ambiguity - never guess silently.

## Scratch mode
To start a session that is not part of this project, say "scratch mode" at the start.
Bootstrap, CONTEXT.md updates, and MEMORY.md writes are skipped. Hooks stay active.

## Skills - auto-trigger rules
| Situation | Skill to read |
|---|---|
| User describes a new feature, component, or idea | `.claude/skills/spec-clarifier/SKILL.md` |
| Creating any new file or module | `.claude/skills/project-structure/SKILL.md` |
| After writing any implementation | `.claude/skills/testing/SKILL.md` |
| Any bug, test failure, or unexpected behavior | `.claude/skills/systematic-debugging/SKILL.md` |
| All tests pass and task is complete | `.claude/skills/commit/SKILL.md` |
| Context filling up or session running long | `.claude/skills/context-optimization/SKILL.md` |
| User wraps up or ends session | `.claude/skills/session-handoff/SKILL.md` |

## Plugins active
- security-guidance: auto-reviews every change for vulnerabilities each turn
- commit-commands: /commit-commands:commit for staged commit with generated message
- pr-review-toolkit: PR review agents on demand
- pyright-lsp: Python type errors and code navigation in real time
- typescript-lsp: TypeScript type errors and code navigation in real time

## Hooks active (deterministic - not dependent on LLM)
- secret-block: blocks precise secret file patterns (see allowlist in hook for exceptions)
- test-gate: runs mirror test for edited file only, not full suite (full suite at commit)
- no-git-add-dot: git add . and git add -A are blocked
- prod-guard: blocks production deploys; dev/local docker push allowed

## Auto-update rules
- Update "Project structure" when a new module or folder is introduced and approved
- Update "Architectural rules" when a new pattern or constraint is established
- Update "Naming conventions" when the first instance of a new file type is created
- Update "Commands" if the user adds or corrects a command
- Always append: <!-- Updated [YYYY-MM-DD]: [what changed and why] -->
- Never remove existing rules without asking first

## Memory boundary
claude-mem captures raw session observations automatically.
MEMORY.md (written by session-handoff skill) captures structured decisions and next steps.
These are complementary - claude-mem for recall, MEMORY.md for decisions.
Do not duplicate decision text into claude-mem; let it capture naturally.

## STOP - ask before:
[From user's answer to question 6]
- Adding any new dependency
- Deleting any file
- Modifying environment variables or secrets
- Anything touching production
```

---

## Step 4 — create CONTEXT.md

```markdown
# CONTEXT.md

<!-- AUTO-MANAGED: Rewritten by Claude at end of each session via session-handoff skill. -->
<!-- Last updated: [YYYY-MM-DD] -->

## Active branch
[git branch --show-current, or "main" if no git yet]

## Session goal
Project initialization complete. Awaiting first feature request.

## Current task
None - ready to start.

## Project status
[List any files that already existed before bootstrap, or "Empty project."]

## Known issues
None.

## Do not touch this session
Nothing locked yet.
```

---

## Step 5 — confirm and hand off

```
Project initialized.

CLAUDE.md  - project rules, structure, skill triggers, hooks and plugins reference
CONTEXT.md - current session state (rewritten each session by session-handoff skill)

Both are maintained by Claude. You won't need to edit them.
Say "scratch mode" at the start of any session you don't want tracked.

What do you want to build first?
```

---

## Rules
- Never write CLAUDE.md or CONTEXT.md before Step 2 is approved.
- Always batch all questions into one message.
- After bootstrap, CLAUDE.md and CONTEXT.md belong to Claude - the user should not need to touch them.
