---
description: Auto-generate tests immediately after every implementation. Triggers when any function, class, route, component, or hook is written or modified.
---

# Testing

## How this skill works

Reads `## Stack` and `## Commands` in `CLAUDE.md` to determine the framework, runner, and file conventions. Nothing is hardcoded here.

---

## Before writing tests

1. Read `## Stack` and `## Commands` in `CLAUDE.md` to confirm:
   - Test framework (pytest, Vitest, Jest, etc.)
   - Test runner command
   - Test file naming convention (if defined)
2. Check existing test files in the project to match their structure and style exactly.
3. If no tests exist yet, propose a convention and add it to `CLAUDE.md` before writing the first test.

---

## When to auto-generate tests

Generate tests as part of the same task — immediately after writing implementation, before moving on. Never defer. Never skip.

Triggers:
- New function or method written
- New class written
- New API route or endpoint written
- New React/Vue/Svelte component written
- New custom hook or composable written
- Existing implementation modified in a way that changes behavior

---

## Universal test structure (framework-agnostic)

Every test file follows this shape regardless of framework:

```
[describe/group/class]: the module or component being tested
  [it/test/def]: happy path — expected inputs, expected output
  [it/test/def]: edge case — boundary, empty, null, or zero
  [it/test/def]: error case — invalid input, thrown exception, failed external call
```

---

## Coverage requirements per unit

| What is being tested | Required cases |
|---|---|
| Pure function | Happy path, edge case, error case |
| Class method | Happy path, invalid state, error propagation |
| API route/endpoint | Success (correct shape), validation failure (400/422), not found (404) |
| React/Vue component | Renders correctly, conditional display, user interaction, callback fired |
| Hook / composable | Initial state, state after event, cleanup on unmount |
| Async function | Resolves correctly, rejects on failure |

---

## What to test vs. not

**Test:**
- Behavior from the caller's perspective
- Return values and side effects
- Error types and messages

**Do not test:**
- Implementation internals (private methods, internal state)
- Third-party library behavior
- Things that require mocking everything to function

**Mocking rule:** Mock at the boundary only — external APIs, databases, file system, system clock. Do not mock modules you own.

---

## CLAUDE.md write-back

If this is the first test in the project, or a new pattern is established:
1. Add test file naming convention to `## Project structure` in `CLAUDE.md`.
2. Add test command to `## Commands` if not already there.
3. Add new mock patterns to `## Architectural rules` if applicable.

---

## After running tests

Always show the result before triggering the commit skill:
```
Tests: 14 passed, 0 failed — all green. Proceeding to commit.
```

If any test fails, fix it first. Do not proceed to commit skill with a red suite.
