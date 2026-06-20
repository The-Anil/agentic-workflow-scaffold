---
description: Reduce context window usage when sessions run long or get expensive. Auto-triggers when many files are loaded, outputs are repetitive, or session has been running 30+ minutes.
---

# Context optimization

## When to trigger

Auto-trigger when ANY of these are true:
- Session has been running 30+ minutes with significant file reads
- You've loaded the same large file into context more than twice
- Outputs are becoming repetitive or confused
- The user mentions slowness, high cost, or repeated answers

---

## Strategies — apply in this priority order

### 1. Reference instead of re-read

Once read, reference by name and line range rather than loading again:
```
Instead of re-reading the whole file:
"The relevant function is [module]:[lines] - I'll read just that section."

Instead of full test output:
"Tests: 23 passed, 0 failed (last run [time])"
```

### 2. Load only what the current task needs

Read the narrowest slice possible:
- A specific function, not the whole module
- A specific line range, not the whole file

### 3. Summarize and drop completed work

When a task is fully complete (implemented + tested + committed), its detail no longer needs to be in active context. Write it to MEMORY.md and move on:
```
"I've written the [feature] summary to memory. Starting fresh context for [next task]."
```

### 4. Partition large independent tasks

If the next task is large and independent of current context, suggest a session break:
```
"The next task doesn't depend on what we've been working on.
I've written a handoff summary - a new session will give you a full context window.
Want to do that, or continue here?"
```

### 5. Run /compact as last resort

If the session must continue and context is critically full:
```
/compact
```

Before running: write any uncommitted decisions to MEMORY.md. Tell the user:
"Running /compact to free up context. CLAUDE.md and CONTEXT.md are preserved."

---

## What always stays in context

- `CLAUDE.md` — project rules and structure
- `CONTEXT.md` — current session state
- The spec file for the active task (`.claude/specs/[current].md`)
- The file currently being edited

---

## What to summarize aggressively

- Full test suite output → pass/fail count only
- Long error stack traces → the relevant frame and message only
- Previously read files not being modified → filename + line reference
- Conversation history about completed tasks → covered by MEMORY.md

---

## After optimizing

Update `CONTEXT.md`:
```markdown
## Context note
Session compacted at [time]. Work before this point is in MEMORY.md.
Active task: [current task]
```

---

## Rule

Optimize for tokens-per-task, not tokens-per-turn.
