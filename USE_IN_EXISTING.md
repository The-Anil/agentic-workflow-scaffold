lets say I have a already half made project, how should I add this scaffold in that and start using it ? what if there's already a claude.md in that, I would like that to be replaced from the calude.md from this workflow

---

Good practical question. Two scenarios depending on what's already in the project.

---

## Adding the scaffold to an existing project

### Step 1 — Copy only the `.claude/` folder

```bash
# From wherever you downloaded/cloned the scaffold
cp -r agentic-workflow-scaffold/.claude  your-existing-project/
cp agentic-workflow-scaffold/.gitignore  your-existing-project/.gitignore  # optional, merge manually if you already have one
```

Do **not** copy `CLAUDE.md` yet — you'll handle that next.

---

### Step 2 — Handle the existing CLAUDE.md

You said you want the scaffold's CLAUDE.md to replace the existing one. But if the existing one has useful project context (stack, structure, conventions), you don't want to throw that away — you want bootstrap to absorb it.

**The right move:**

```bash
# Rename the existing one so bootstrap can reference it
mv your-existing-project/CLAUDE.md your-existing-project/CLAUDE.old.md

# Copy in the scaffold seed
cp agentic-workflow-scaffold/CLAUDE.md your-existing-project/CLAUDE.md
```

Now the seed `CLAUDE.md` is in place (contains `UNINITIALIZED`, triggers bootstrap on first session), and `CLAUDE.old.md` is sitting there for Claude to read during bootstrap.

---

### Step 3 — First session — tell Claude about the existing project

Open Claude Code in the project:

```bash
claude
```

Bootstrap triggers automatically. When Claude asks the 6 questions, add this at the end of your answer:

```
Also — there's a CLAUDE.old.md in the project root with the previous 
setup. Please read it and incorporate anything relevant into the new 
CLAUDE.md you're about to write.
```

Claude will read `CLAUDE.old.md`, extract the useful parts (stack, structure, conventions, existing commands), and fold them into the new `CLAUDE.md` it writes. After bootstrap completes:

```bash
# Clean up the old file
rm your-existing-project/CLAUDE.old.md
```

---

### Step 4 — Tell Claude about existing code

After bootstrap writes `CLAUDE.md` and `CONTEXT.md`, immediately follow up with:

```
Before we build anything new, scan the existing codebase and update 
CLAUDE.md's project structure section to reflect what's actually there. 
Also note any patterns or conventions you observe in the existing code 
in the architectural rules section.
```

Claude will read the existing files, infer the conventions, and update `CLAUDE.md` to accurately reflect the real state of the project. This is important — otherwise the project-structure skill will try to enforce a proposed layout that doesn't match what already exists.

---

### Step 5 — Windows path fix (if on Windows)

Same as a new project — open `.claude/settings.json` and replace `python3` with `python` everywhere.

---

## What you end up with

After these steps the project is in the same state as if you'd started it fresh with the scaffold — `CLAUDE.md` reflects the real project, `CONTEXT.md` describes current state, hooks are active, skills are loaded. The only difference is the existing code was already there when bootstrap ran, which is fine.

---

## The short version for a half-made project

```
1. cp -r scaffold/.claude  your-project/
2. mv your-project/CLAUDE.md  your-project/CLAUDE.old.md
3. cp scaffold/CLAUDE.md  your-project/CLAUDE.md
4. claude  (bootstrap runs, tell it to read CLAUDE.old.md)
5. After bootstrap: ask Claude to scan existing code and update CLAUDE.md structure
6. rm CLAUDE.old.md
```

Six steps, one session, then the workflow runs exactly as designed going forward.