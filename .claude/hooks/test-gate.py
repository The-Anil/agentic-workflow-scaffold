#!/usr/bin/env python3
"""
Hook: test-gate
Event: PostToolUse (Write | Edit)

Runs the minimal relevant tests after a source file edit, not the full suite.
Strategy:
  1. Try to run only the test file that mirrors the edited source (fast, ~2-5s).
  2. If no mirror test exists, skip silently — don't punish files without tests yet.
  3. Full suite is NOT run here; the commit skill handles that before committing.

Reads test command from CLAUDE.md ## Commands section.
Exit 1 = tests failed (Claude must fix). Exit 0 = passed or skipped.
"""
import sys
import json
import subprocess
import re
import os
from pathlib import Path

data = json.load(sys.stdin)
tool_input = data.get("tool_input", {})
path = (
    tool_input.get("file_path", "")
    or tool_input.get("path", "")
    or tool_input.get("target_file", "")
)

if not path:
    sys.exit(0)

# Normalize to forward slashes for consistent matching
path = path.replace("\\", "/")

# Never trigger on these file types
SKIP_PATTERNS = [
    ".test.", ".spec.", "_test.", "test_",
    "SKILL.md", "CLAUDE.md", "CONTEXT.md", "MEMORY.md",
    "settings.json", ".gitignore", "README",
    "package.json", "pyproject.toml", "requirements",
    "tsconfig", "vite.config", "jest.config", "eslint",
    ".claude/", ".github/",
]

if any(p in path for p in SKIP_PATTERNS):
    sys.exit(0)

SOURCE_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".rb"}
if Path(path).suffix not in SOURCE_EXTENSIONS:
    sys.exit(0)


def find_python_cmd():
    """Find the correct python command for this platform."""
    for cmd in ("python3", "python", "py"):
        try:
            result = subprocess.run(
                [cmd, "-c", "import sys; print(sys.version_info.major)"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0 and result.stdout.strip() == "3":
                return cmd
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return None


def get_test_config():
    """Read test command and framework from CLAUDE.md ## Commands section."""
    claude_md = Path("CLAUDE.md")
    if not claude_md.exists():
        return None, None, None

    content = claude_md.read_text(encoding="utf-8")
    match = re.search(r"## Commands\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
    if not match:
        return None, None, None

    for line in match.group(1).splitlines():
        line = line.strip().lstrip("-").strip()
        line_lower = line.lower()

        if "pytest" in line_lower:
            cmd = line.split("#")[0].strip()
            cwd = None
            if "cd " in cmd:
                parts = cmd.split("&&")
                for part in parts:
                    if part.strip().startswith("cd "):
                        cwd = part.strip()[3:].strip()
                        break
                cmd = parts[-1].strip()
            return "pytest", cmd, cwd

        if any(kw in line_lower for kw in ["npm test", "yarn test", "pnpm test", "vitest", "jest"]):
            cmd = line.split("#")[0].strip()
            cwd = None
            if "cd " in cmd:
                parts = cmd.split("&&")
                for part in parts:
                    if part.strip().startswith("cd "):
                        cwd = part.strip()[3:].strip()
                        break
                cmd = parts[-1].strip()
            framework = "vitest" if "vitest" in line_lower else "jest"
            return framework, cmd, cwd

    return None, None, None


def find_mirror_test(source_path, framework):
    """
    Try to locate the test file that corresponds to the edited source.
    Returns the test file path string if found, else None.
    """
    p = Path(source_path)
    stem = p.stem
    suffix = p.suffix
    parent = p.parent

    if framework == "pytest":
        candidates = [
            parent / f"test_{stem}.py",
            parent / "__tests__" / f"test_{stem}.py",
            parent / "tests" / f"test_{stem}.py",
        ]
    else:
        candidates = [
            parent / f"{stem}.test{suffix}",
            parent / f"{stem}.spec{suffix}",
            parent / "__tests__" / f"{stem}.test{suffix}",
            parent / "__tests__" / f"{stem}.spec{suffix}",
        ]

    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return None


def run_targeted_test(framework, base_cmd, cwd, test_file):
    """Run only the mirror test file with a short timeout."""
    timeout = 30  # seconds — fast feedback, not a full suite

    if framework == "pytest":
        cmd = f"pytest {test_file} --tb=short -q --no-header"
    elif framework in ("vitest", "jest"):
        # Pass the test file as a filter pattern
        cmd = f"{base_cmd} -- --run {test_file}"
    else:
        return None

    try:
        return subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd or os.getcwd(),
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return "timeout"


# --- Main ---

framework, base_cmd, cwd = get_test_config()

if not framework:
    sys.exit(0)

test_file = find_mirror_test(path, framework)

if not test_file:
    # No mirror test yet — skip silently, don't penalise new files
    sys.exit(0)

result = run_targeted_test(framework, base_cmd, cwd, test_file)

if result == "timeout":
    print(json.dumps({
        "systemMessage": (
            f"Mirror test for {path} timed out after 30s. "
            "Check for hanging tests or increase the timeout in test-gate.py."
        )
    }))
    sys.exit(1)

if result is None:
    sys.exit(0)

if result.returncode != 0:
    output = (result.stdout + result.stderr)[-2000:]
    print(json.dumps({
        "systemMessage": (
            f"Tests failed for {path} (ran {test_file}).\n\n"
            f"{output}\n\n"
            "Fix the failures before continuing. Full suite will run at commit time."
        )
    }))
    sys.exit(1)

sys.exit(0)
