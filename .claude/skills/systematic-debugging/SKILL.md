---
description: Four-phase debugging methodology with mandatory root cause analysis. Auto-triggers when investigating any bug, test failure, or unexpected behavior. Rule: NO FIX WITHOUT ROOT CAUSE FIRST.
---

# Systematic debugging

## The one rule

**NO FIX WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

Never apply a symptom-focused patch that masks the underlying problem. Understand WHY something fails before attempting to fix it.

---

## Four phases — run in sequence, do not skip

### Phase 1 — Observe the symptom

- Where exactly does the error manifest? (file, line, function, test case)
- What is the exact error message? (copy verbatim, do not paraphrase)
- What is the expected behavior vs. actual behavior?
- Is this consistently reproducible or intermittent?

Output: a single precise statement of what is broken.

### Phase 2 — Find the immediate cause

- Which code directly produces the error?
- What value or state leads to that code path?
- Read only the minimum code needed — do not load entire modules.

Output: the specific line or expression causing the failure.

### Phase 3 — Trace the call chain upward

- Ask: "What called this, and what passed in the bad value?"
- Follow the chain one level at a time.
- Stop when you find the point where the incorrect value was introduced.
- Do not jump to the fix until the chain is fully traced.

Output: the root origin of the bad value or bad state.

### Phase 4 — Confirm root cause before fixing

- State the root cause explicitly:
  ```
  Root cause: [specific function/module] passes [bad value] to [other function]
  because [reason]. This causes [symptom].
  ```
- Ask: "Does fixing this root cause resolve the symptom without introducing new problems?"
- If yes — fix at the root.
- If no — explain the trade-off before proceeding.

---

## What not to do

- Do not add `try/except` or `try/catch` to hide an error without understanding it
- Do not change logic "to see if it helps"
- Do not assume the most obvious-looking line is the cause — trace it
- Do not fix and immediately move on — verify the fix resolves the original symptom

---

## After fixing

1. Run the full test suite — not just the failing test.
2. Confirm the original symptom is gone.
3. Check for regressions in adjacent code.
4. Then trigger the commit skill with a message that explains the root cause in the body.

---

## Template for the commit body after a fix

```
fix(scope): short description of what was fixed

Root cause: [what was actually wrong and why].
This caused [symptom] when [condition].

Fix: [what was changed and why this addresses root cause].
[Any follow-up tasks or watch points.]
```
