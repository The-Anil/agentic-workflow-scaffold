# Agentic Workflow Scaffold

A reusable Claude Code setup that turns vague feature requests into implemented, tested, and committed code — with minimal hand-holding.

You describe a feature. Answer 2–3 clarifying questions. Say "looks good". Say "commit". Everything in between is handled automatically.

---

## What this is

A project-agnostic scaffold for Claude Code consisting of:

- **5 Python hook scripts** — deterministic guardrails that run regardless of what the LLM decides
- **8 skill files** — markdown instructions that Claude loads on demand based on the task type
- **A seed `CLAUDE.md`** — triggers a bootstrap interview on first session, then Claude maintains it forever
- **A baseline `.gitignore`** and `specs/` directory

Nothing in the scaffold is hardcoded to a specific project, language, or framework. The bootstrap skill interviews you on first session and writes all project-specific config into `CLAUDE.md` automatically.

---

## How the workflow works

```
You type a feature request
       ↓
spec-clarifier asks ≤3 questions
       ↓
You answer → spec file written → you approve
       ↓
project-structure enforces correct folder placement
       ↓
Implementation written
       ↓
test-gate hook auto-runs mirror tests after each file edit
       ↓
testing skill writes full test coverage
       ↓
All tests pass → commit skill drafts conventional commit → you approve
       ↓
git commit runs
       ↓
session-handoff rewrites CONTEXT.md + updates MEMORY.md
       ↓
Next session opens with full context on where you left off
```

Your inputs across the entire flow: the feature description, answers to ≤3 questions, "looks good", and "commit".

---

## File structure

```
agentic-workflow-scaffold/
├── CLAUDE.md                          # Seed file — Claude rewrites this on first session
├── SETUP.md                           # Step-by-step setup instructions
├── .gitignore                         # Baseline: .env, .env.*, local Claude settings
└── .claude/
    ├── settings.json                  # Wires all 5 hooks to their scripts
    ├── hooks/
    │   ├── secret-block.py            # PreToolUse — blocks .env, *.key, *.pem reads/writes
    │   ├── no-git-add-dot.py          # PreToolUse — blocks git add . and git add -A
    │   ├── prod-guard.py              # PreToolUse — blocks production deploy commands
    │   ├── test-gate.py               # PostToolUse — runs mirror test after source file edits
    │   └── session-end-reminder.py    # Stop — reminds Claude to run session-handoff
    ├── skills/
    │   ├── bootstrap/                 # First session only — interviews you, writes CLAUDE.md + CONTEXT.md
    │   ├── spec-clarifier/            # Vague request → ≤3 questions → spec file → approval
    │   ├── project-structure/         # File creation → reads CLAUDE.md → correct folder placement
    │   ├── testing/                   # After implementation → tests generated alongside
    │   ├── systematic-debugging/      # Any bug → 4-phase root cause before fix
    │   ├── commit/                    # Tests green → conventional commit drafted for approval
    │   ├── session-handoff/           # Session end → CONTEXT.md rewritten, MEMORY.md updated
    │   └── context-optimization/      # Long sessions → token reduction strategies
    └── specs/                         # Auto-written by spec-clarifier, one file per feature
```

---

## Hooks vs. skills

| | Hooks | Skills |
|---|---|---|
| What they are | Python scripts | Markdown files |
| When they run | Automatically on Claude Code lifecycle events | When Claude recognises a matching task type |
| Depend on LLM | No — deterministic | Yes — LLM reads and follows them |
| Purpose | Enforce rules that must never be bypassed | Guide the LLM's workflow and decisions |
| Examples | Block .env reads, block `git add .` | Write specs, generate tests, draft commits |

---

## What is automated vs. what you do

| Automated | You do |
|---|---|
| Spec clarification (≤3 questions) | Describe the feature |
| Project structure enforcement | Answer clarifying questions |
| Test generation alongside implementation | Say "looks good" on the spec |
| Mirror test run after every file edit | Say "commit" to approve the draft |
| Full test suite at commit time | Say "done" or "bye" to end session |
| Conventional commit drafted for approval | — |
| CONTEXT.md rewritten each session | — |
| MEMORY.md updated with decisions | — |
| CLAUDE.md maintained as project evolves | — |

---

## Scratch mode

For sessions that aren't part of project development (analysis, exploration, reviewing code) — say **"scratch mode"** at the start of the session.

- Bootstrap does not run
- CONTEXT.md is not updated
- MEMORY.md is not written
- All hooks still run (security guardrails stay on)

The next normal session picks up exactly where the last project session left off.

---

## Setup

See **[SETUP.md](./SETUP.md)** for the complete step-by-step guide including:

- Prerequisites (Claude Code, Node.js 18+, Python 3, Git)
- Windows path fix for `settings.json`
- claude-mem installation (persistent cross-session memory)
- claude-token-lens installation (real-time token cost visibility)
- Plugin installation inside Claude Code
- Bootstrap walkthrough (first session)

---

## Using this as a template for a new project

This repo is configured as a GitHub template. On the repo page, click **"Use this template"** → **"Create a new repository"**. GitHub creates a new repo with all scaffold files and a clean commit history — no link back to this repo.

```bash
# Clone your new project repo
git clone https://github.com/you/your-new-project
cd your-new-project

# Windows only: open .claude/settings.json
# Replace every "python3" with "python"

# Install claude-mem (once per machine)
npx --yes claude-mem install

# Open Claude Code — bootstrap runs automatically on first message
claude
```

Steps after the first project (claude-mem, plugins) are per-machine, not per-project. Starting a second project is just "Use this template" → clone → `claude`.

---

## One-time global installs (per machine, not per project)

```bash
# Persistent cross-session memory
npx --yes claude-mem install

# Token cost visibility (run in a separate terminal during sessions)
npm install -g claude-token-lens
```

Inside Claude Code (run once per machine):

```
/plugin install security-guidance@claude-plugins-official
/plugin install commit-commands@claude-plugins-official
/plugin install pr-review-toolkit@claude-plugins-official
/plugin install pyright-lsp@claude-plugins-official
/plugin install typescript-lsp@claude-plugins-official
/plugin marketplace add anthropics/claude-plugins-community
```

---

## Customising the hooks

The hooks ship with sensible defaults but are easy to adjust:

**`secret-block.py`** — has an `ALLOWLIST` at the top for legitimate files that match secret patterns (e.g. `secrets_manager.py`). Add to it as your project grows.

**`test-gate.py`** — has a `SKIP_PATTERNS` list for files that should never trigger a test run. Add patterns if the hook fires on files it shouldn't.

**`prod-guard.py`** — has an allowlist for dev/local Docker registry pushes (`localhost:`, `dev.`, `staging.`). Add your own dev registry patterns if needed.

---

## What Claude maintains automatically

After bootstrap, you should not need to manually edit these files:

| File | Written by | When |
|---|---|---|
| `CLAUDE.md` | bootstrap skill (first session), then Claude | First session + whenever new patterns emerge |
| `CONTEXT.md` | session-handoff skill | End of every session |
| `~/.claude/projects/[name]/memory/MEMORY.md` | session-handoff skill | End of every session |
| `.claude/specs/[feature].md` | spec-clarifier skill | Before every implementation |

---

## Requirements

- Claude Code (claude.ai/download)
- Claude Pro, Max, or API account
- Node.js 18+
- Python 3 (added to PATH)
- Git