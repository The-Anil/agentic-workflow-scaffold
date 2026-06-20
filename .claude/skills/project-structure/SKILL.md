---
description: Enforce correct folder and file placement when creating any new file, module, component, route, or test. Auto-triggers on file creation.
---

# Project structure

## How this skill works

Reads `## Project structure` in `CLAUDE.md` and enforces it.
No folder layout is hardcoded here — the layout lives in `CLAUDE.md` and evolves with the project.

---

## Before creating any file

1. Read `## Project structure` in `CLAUDE.md`.
2. Identify which category the new file belongs to.
3. Determine the correct path.
4. If the path is ambiguous or category doesn't exist yet, propose it:
   ```
   This is the first [type] file. I'll place it at [path] and add it to CLAUDE.md. OK?
   ```
5. Wait for approval on any new locations before creating.

---

## Universal rules (stack-agnostic)

**Placement:**
- Tests live adjacent to or mirroring the source they test — never in a disconnected top-level folder unless `CLAUDE.md` defines it that way.
- Shared utilities go in a shared/common folder only when two or more modules need them. Never pre-emptively.
- New features get their own module — do not append to unrelated existing files.
- Configuration and environment handling go in a dedicated config file.

**Naming:**
- Match the casing and suffix pattern of the nearest existing file of the same type.
- If no pattern exists yet, use the language's idiomatic convention:
  - Python: `snake_case` files and functions, `PascalCase` classes
  - TypeScript/JS: `camelCase` files and functions, `PascalCase` components and classes
  - CSS: `kebab-case` class names
- Never create catch-all files named `utils`, `helpers`, or `misc` — name by what they do.

**Depth:** Never nest more than 3 levels deep unless the project already does so.

**Boundaries:** Always respect architectural rules from `## Architectural rules` in `CLAUDE.md`.

---

## When CLAUDE.md has no structure defined

If `## Project structure` is missing or empty:
1. Do not invent a structure.
2. Say: "No project structure is defined yet. Let me propose one based on your stack, then add it to CLAUDE.md."
3. Propose, wait for approval, write to `CLAUDE.md`, then create files.

---

## CLAUDE.md write-back

When a new file type, folder, or module is created that isn't already in the structure:
1. Add it to `## Project structure` in `CLAUDE.md` with a one-line comment.
2. Append: `<!-- Updated [YYYY-MM-DD]: added [path] for [reason] -->`

---

## After creating files

Always list what was created with full paths:
```
Created:
  src/features/auth/login.py       (new feature module)
  src/features/auth/test_login.py  (co-located test)

CLAUDE.md updated: src/features/ pattern documented.
```
