---
description: Summarize the session, rewrite CONTEXT.md, and write structured decisions to MEMORY.md. Auto-triggers when user wraps up or context is approaching its limit. Does NOT run in scratch mode.
---

# Session handoff

## When to trigger
- User says: "done", "that's it", "wrap up", "end session", "see you", "bye", "good night"
- Context window is filling and work needs to continue in a new session
- A major milestone is complete (full feature implemented, tested, committed)

## When NOT to trigger
- The session was started in scratch mode
- No project work was done (only analysis, exploration, or throwaway tasks)

If in scratch mode, just say: "Scratch mode session — nothing written to memory or CONTEXT.md."

---

## Step 1 — write the MEMORY.md entry

**File location:** `~/.claude/projects/[project-name]/memory/MEMORY.md`

Determine project name from:
1. First line of `## Project` in `CLAUDE.md`
2. Otherwise: the git repo folder name

Create the file and directory if they don't exist. Prepend - newest entry at top.

```markdown
## [YYYY-MM-DD] - [one-line summary of what this session accomplished]

### Built / changed
- `[file path]` - [what changed and why, one line each]

### Decisions made
- [Decision]: [Reasoning - why this approach over alternatives]

### Patterns established
- [Pattern name]: [What it is, where it lives in the project]

### Known issues / deferred work
- [Issue]: [Enough context to act without re-reading the conversation]

### Commits this session
- [type(scope): subject]

### Next steps
- [ ] [Specific enough to start immediately without re-reading history]
```

Keep each entry under 50 lines. Decisions and next steps are more valuable than code summaries — the code is in git, WHY you made a choice is not.

---

## Step 2 — rewrite CONTEXT.md

Replace the entire contents of `CONTEXT.md`:

```markdown
# CONTEXT.md

<!-- AUTO-MANAGED: Rewritten by Claude at end of each session via session-handoff skill. -->
<!-- Last updated: [YYYY-MM-DD] -->

## Active branch
[git branch --show-current]

## Project status
[2-3 sentences: what's built, what's in progress, what's blocked]

## Next session goal
[First next step from MEMORY.md - what to start immediately on next open]

## Pending tasks
- [ ] [From next steps in MEMORY.md]

## Known issues
- [From known issues above. "None." if clear.]

## Do not touch
- [Active WIP, files mid-refactor, anything to leave alone]
```

---

## Step 3 — update CLAUDE.md if needed

If new patterns, conventions, or rules emerged this session:
1. Add to the relevant section.
2. Append: `<!-- Updated [YYYY-MM-DD]: [what and why] -->`
3. Tell the user what was updated.

---

## Step 4 — confirm to the user

```
Session wrapped up.

[list commits made this session]

CONTEXT.md rewritten for next session.
Memory updated.

Next session starts with:
-> [first next step]

Say "scratch mode" at the start of any session you don't want tracked.
```

---

## Rules
- Write MEMORY.md and rewrite CONTEXT.md before ending. Not optional.
- Decisions are more valuable than code summaries - the code is in git.
- Next steps must be specific enough to act on without reading this conversation.
- CONTEXT.md is a briefing for a fresh Claude with only CLAUDE.md and CONTEXT.md to go on.
- Merge into MEMORY.md (newest at top), never overwrite entirely.