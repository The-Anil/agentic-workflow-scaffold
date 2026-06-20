# Agentic Workflow — Setup & Usage Guide

---

## Prerequisites

| Tool | Check | Install |
|---|---|---|
| Claude Code | `claude --version` | https://claude.ai/download |
| Node.js 18+ | `node --version` | https://nodejs.org |
| Python 3 | `python --version` | https://python.org (tick "Add to PATH" on Windows) |
| Git | `git --version` | https://git-scm.com |

---

## Part 1 — Setup (once per project)

### Step 1 — Copy the scaffold

Copy the entire contents of this package into your project root:

```
your-project/
  .claude/
    hooks/          (5 Python hook scripts)
    skills/         (8 SKILL.md files)
    specs/          (empty dir, spec-clarifier writes here)
    settings.json
  .gitignore
  CLAUDE.md
```

### Step 2 — Init git

```
git init
```

The `.gitignore` is already in the scaffold — it excludes `.env`, `.env.*`, and `.claude/settings.local.json`.

### Step 3 — Windows path fix in settings.json

Open `.claude/settings.json`. Replace every occurrence of:
```
python3
```
with:
```
python
```

Use Find & Replace in VS Code (Ctrl+H). On Mac/Linux, skip this step.

### Step 4 — Install claude-token-lens

```
npm install -g claude-token-lens
```

Run in a separate terminal during sessions to monitor token burn rate:
```
claude-token-lens
```

### Step 5 — Install plugins inside Claude Code

Open Claude Code in your project directory:
```
claude
```

Then run these commands inside the session:

```
/plugin install security-guidance@claude-plugins-official
/plugin install commit-commands@claude-plugins-official
/plugin install pr-review-toolkit@claude-plugins-official
/plugin install pyright-lsp@claude-plugins-official
/plugin install typescript-lsp@claude-plugins-official
/plugin marketplace add anthropics/claude-plugins-community
/reload-plugins
```

If any plugin says "not found":
```
/plugin marketplace update claude-plugins-official
```
Then retry the install.

### Step 6 — Bootstrap (first project session only)

Start Claude Code and say anything. Claude detects `UNINITIALIZED` in `CLAUDE.md`, runs the bootstrap skill, and asks you 6 questions in one message. You answer, approve the proposed structure, and Claude writes the full `CLAUDE.md` and `CONTEXT.md`. You never touch those files again.

---

## Part 2 — Scratch mode (sessions outside the project)

Sometimes you want to open Claude Code in a project directory to analyze, explore, or ask questions — without it being treated as project development. Bootstrap should not run, nothing should be written to memory or CONTEXT.md.

**To start a scratch session, say this at the beginning:**

```
scratch mode
```

or:

```
this is not a project session
```

Claude will confirm scratch mode is active and help with whatever you asked. Hooks (secret-block, prod-guard, etc.) still run — security guardrails stay on. Nothing is written to CLAUDE.md, CONTEXT.md, or MEMORY.md.

**Examples of when to use scratch mode:**
- Analyzing the project setup (like this conversation)
- Reading and understanding existing code without building anything
- Exploring a library or API before deciding whether to use it
- Running one-off queries against the codebase
- Asking architectural questions before committing to an approach

To return to normal project sessions, just start the next session normally (no "scratch mode").

---

## Part 3 — Usage walkthrough (small feature, end to end)

This is how a typical feature goes from idea to committed code.

---

### Scenario: adding a `/health` endpoint to a FastAPI backend

**You open Claude Code and type:**

```
Add a health check endpoint
```

---

**What Claude does — Step 1: spec-clarifier triggers**

Claude reads CLAUDE.md, sees this is vague, and asks at most 3 questions:

```
Before I build this, a couple of questions:

1. Should /health return just a 200 OK, or include service status details
   (db connection, uptime, version)?
2. Does it need authentication, or should it be publicly accessible?
```

**You answer:**

```
Just 200 OK with a JSON body showing version and uptime. No auth needed.
```

---

**What Claude does — Step 2: spec written**

Claude writes `.claude/specs/health-endpoint.md` and shows it to you:

```
# Feature: health endpoint

## What it does
GET /health returns 200 with {"status": "ok", "version": "...", "uptime_seconds": N}.
No authentication required. Intended for load balancer health checks.

## Constraints
- Must respond in under 100ms
- No database call involved

## Out of scope
- Dependency health checks (db, redis)
- Authentication

## Success criteria
- [ ] GET /health returns 200
- [ ] Response body contains status, version, uptime_seconds
- [ ] pytest passes for the new route

## Files likely affected
- backend/app/api/routes/health.py  (new)
- backend/app/main.py               (register router)
- backend/tests/test_api/test_health.py  (new)

Spec written — does this look right before I start?
```

**You say:** `looks good`

---

**What Claude does — Step 3: project-structure triggers**

Claude reads `## Project structure` in CLAUDE.md, confirms the correct paths, and creates:

```
Created:
  backend/app/api/routes/health.py      (new route)
  backend/tests/test_api/test_health.py (co-located test)

CLAUDE.md updated: health route added to project structure.
```

---

**What Claude does — Step 4: implements**

Writes the minimal implementation:

```python
# backend/app/api/routes/health.py
import time
from fastapi import APIRouter
from app.config import settings

router = APIRouter()
START_TIME = time.time()

@router.get("/health")
async def health():
    return {
        "status": "ok",
        "version": settings.VERSION,
        "uptime_seconds": int(time.time() - START_TIME),
    }
```

Registers it in `main.py`.

---

**What Claude does — Step 5: testing triggers**

Immediately writes tests alongside:

```python
# backend/tests/test_api/test_health.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

class TestHealthEndpoint:
    async def test_returns_200(self, client):
        response = await client.get("/health")
        assert response.status_code == 200

    async def test_response_shape(self, client):
        response = await client.get("/health")
        body = response.json()
        assert body["status"] == "ok"
        assert "version" in body
        assert isinstance(body["uptime_seconds"], int)

    async def test_no_auth_required(self, client):
        response = await client.get("/health")
        assert response.status_code != 401
```

---

**What happens automatically — test-gate hook**

After Claude writes `health.py`, the test-gate hook fires automatically. It finds `test_health.py` (the mirror file) and runs just that test file — not the whole suite:

```
pytest backend/tests/test_api/test_health.py --tb=short -q
```

If tests pass: silent, Claude continues.
If tests fail: Claude sees the failure and fixes before moving on.

---

**What Claude does — Step 6: commit skill triggers**

Tests are green. Claude runs the full suite, then shows the commit draft:

```
====================================
COMMIT DRAFT - awaiting your approval
====================================

git commit -m "feat(api): add GET /health endpoint with uptime and version

Load balancer health checks require a lightweight endpoint with no auth.
Returns status, app version, and uptime_seconds. No DB call involved.

Spec: .claude/specs/health-endpoint.md"

Files staged:
  backend/app/api/routes/health.py          (+18 lines)
  backend/app/main.py                       (+2 lines)
  backend/tests/test_api/test_health.py     (+24 lines)

Checks:
  OK pytest - 31 passed
  OK ruff check
====================================
Say "commit" to run this, or tell me what to change.
```

**You say:** `commit`

Git commit runs. Done.

---

**End of session — say "done" or "bye"**

Session-handoff skill runs automatically:

- Writes a structured entry to `~/.claude/projects/[project]/memory/MEMORY.md`
- Rewrites `CONTEXT.md` for next session:

```markdown
## Active branch
main

## Project status
Health endpoint complete and committed. Three agent personas
(ProductManager, SecurityAuditor, PerformanceOptimizer) are next.

## Next session goal
Implement the ProductManager agent persona

## Pending tasks
- [ ] ProductManager agent - proposes features, writes user stories
- [ ] SecurityAuditor agent - attacks proposals for vulnerabilities
- [ ] PerformanceOptimizer agent - critiques compute cost

## Known issues
None.
```

Next session, Claude opens with full context on where you left off. No re-explaining needed.

---

## What you did in this entire workflow

1. Typed: "Add a health check endpoint"
2. Answered 2 clarifying questions
3. Said: "looks good"
4. Said: "commit"
5. Said: "done"

Everything else was handled automatically.

---

## Troubleshooting

**Hooks not running**
Open a terminal and run `python --version`. If Python isn't found, reinstall it and add to PATH. Restart Claude Code after fixing.

**Plugin not found**
Run `/plugin marketplace update claude-plugins-official` then retry.

**test-gate firing on wrong files**
Add the file pattern to `SKIP_PATTERNS` in `.claude/hooks/test-gate.py`.

**secret-block blocking a legitimate file**
Add the file name (without extension) to the `ALLOWLIST` in `.claude/hooks/secret-block.py`.

**Accidentally bootstrapped in an analysis session**
Close the session. For future analysis sessions, say "scratch mode" as your first message.