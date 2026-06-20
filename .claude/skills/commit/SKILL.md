---
description: Draft a conventional commit after tests pass. Auto-triggers when a task is complete and all tests are green. Always drafts for user approval — never commits automatically.
---

# Commit

## Trigger condition

Activate when ALL are true:
1. Implementation is complete
2. Tests are written and passing
3. Diff contains only files related to this task

Do NOT trigger if any test is failing or unrelated files are modified.

---

## Pre-commit checks — run in this order

Read `## Commands` in `CLAUDE.md` for the exact commands:

```
1. Test suite     → from ## Commands in CLAUDE.md
2. Lint           → from ## Commands in CLAUDE.md (if defined)
3. Type check     → from ## Commands in CLAUDE.md (if defined)
```

Fix any failure before drafting. Do not draft with a red suite.

---

## Staging — surgical only

Stage only files changed by this task. Never `git add .`:

```bash
git add [specific file] [specific file]
git diff --staged    # verify before drafting
```

Unstage unrelated files:
```bash
git restore --staged path/to/unrelated/file
```

---

## Commit message format

**Subject line** (50 chars max, imperative mood):
```
type(scope): short description
```

**Body** (required for `feat` and `fix`):
```
Explain WHY this change was made.
What problem does it solve? What was missing or broken?
Side effects, follow-up tasks, or significant decisions.
```

**Footer** (optional):
```
Spec: .claude/specs/[feature-name].md
```

---

## Types

| Type | Use when |
|---|---|
| `feat` | New user-facing or system behavior |
| `fix` | Bug fix in existing behavior |
| `refactor` | Code change with no behavior change |
| `test` | Adding or modifying tests only |
| `chore` | Deps, config, tooling, build |
| `docs` | Documentation, comments, README |

**Scope:** Use the module, feature area, or layer name from `CLAUDE.md`'s project structure.

---

## Draft format — always show this, never skip

```
====================================
COMMIT DRAFT - awaiting your approval
====================================

git commit -m "type(scope): subject line

Body explaining why this change was made.
Any side effects or follow-up tasks noted here."

Files staged:
  [file path]  (+N lines)
  [file path]  (+N lines)

Checks:
  OK [test command] - N passed
  OK [lint command] (if applicable)
====================================
Say "commit" to run this, or tell me what to change.
```

Wait for "commit", "go", "looks good", or equivalent. Never run `git commit` without explicit approval.

---

## After committing

Update `CONTEXT.md` — mark task complete, set next:

```markdown
## Completed this session
- [type(scope): subject] - [one-line summary]

## Current task
[Next task, or "Awaiting next feature request"]
```

---

## Rules
- Imperative mood: "add" not "added", "fix" not "fixed"
- Never mention filenames in subject — the diff shows that
- Never use: "WIP", "update", "changes", "cleanup", "misc"
- Body explains WHY — diff shows what
- One logical change per commit — if two unrelated things changed, make two commits
