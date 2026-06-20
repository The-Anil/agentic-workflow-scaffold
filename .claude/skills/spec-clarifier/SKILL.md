---
description: Clarify vague feature requests into structured specs before any implementation. Auto-triggers when the user describes a new feature, component, endpoint, or idea without clear constraints or verifiable success criteria.
---

# Spec clarifier

## When to trigger
Activate when the request is any of:
- A new feature described in plain English without implementation detail
- A new component, route, module, or integration with no defined contract
- Any description missing at least one verifiable success criterion
- A task where scope, constraints, or expected behavior would require guessing

Do NOT trigger for:
- Bug fixes where expected behavior is already clear
- Refactors with an explicit before/after description
- Tasks scoped to a single function or file with no ambiguity

---

## Process

1. Read `CLAUDE.md` — understand the project context, stack, and structure before forming questions.
2. Identify the single biggest unknown that would change the implementation.
3. Ask a maximum of 3 questions — no more. Prioritize:
   - Behavior and control flow first
   - Data shape / API contract second
   - UI/UX third
4. Wait for answers. Do not write code or create files before receiving them.
5. Write the spec to `.claude/specs/[kebab-case-feature-name].md`.
6. Show the spec: "Spec written — does this look right before I start?" Wait for approval or amendments.
7. Proceed with implementation.

---

## Spec output format

```markdown
# Feature: [name]

## What it does
[One paragraph — behavior from user or system perspective. No implementation detail.]

## Constraints
- [Hard limits, technical constraints, backwards-compatibility requirements]

## Out of scope
- [Explicitly not included in this task]

## Success criteria
- [ ] [Verifiable — e.g. "all tests pass", "POST /x returns 200 with id field"]
- [ ] [Another criterion — observable behavior, not a quality adjective]

## Files likely affected
- [Use paths from CLAUDE.md project structure — no invented paths]

## Open questions
- [Anything still unresolved — flag for follow-up]
```

---

## CLAUDE.md write-back

After implementing a feature, if any of the following are true, update `CLAUDE.md`:

| Discovery | Section to update |
|---|---|
| New folder or module type created | `## Project structure` |
| New architectural pattern established | `## Architectural rules` |
| New naming convention emerged | `## Naming conventions` |
| New command used | `## Commands` |

Append on the changed line:
```
<!-- Updated [YYYY-MM-DD]: added [what] because [why] -->
```

Never remove or overwrite existing rules — only extend.

---

## Rules
- Never write code before the spec is approved.
- Never ask more than 3 questions.
- Success criteria must be checkable — not adjectives, but observable behaviors or passing commands.
- Use `CLAUDE.md`'s defined structure for file paths. Do not invent paths.
- If the request would violate a STOP rule in `CLAUDE.md`, say so immediately before continuing.
