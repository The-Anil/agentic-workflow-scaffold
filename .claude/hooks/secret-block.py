#!/usr/bin/env python3
"""
Hook: secret-block
Event: PreToolUse (Read | Write | Edit)
Blocks access to files that are likely to contain raw credentials.
Uses precise path matching to avoid false positives on legitimate code files.
Exit 2 = blocked. Exit 0 = allowed.
"""
import sys
import json
import re
from pathlib import Path

data = json.load(sys.stdin)
tool_input = data.get("tool_input", {})
raw_path = (
    tool_input.get("file_path", "")
    or tool_input.get("path", "")
    or tool_input.get("target_file", "")
)

if not raw_path:
    sys.exit(0)

path = raw_path.replace("\\", "/").lower()
filename = Path(path).name

# Files explicitly allowed even if they match a pattern below.
# Add to this list as your project grows legitimate uses.
ALLOWLIST = [
    "secrets_manager",       # e.g. secrets_manager.py — code that reads secrets
    "credentials_test",      # test file for credential-handling code
    "credentials_helper",
    "secret_service",        # service layer, not raw creds
    "secret_store",
    ".env.example",          # committed template, no real values
    ".env.test",             # test fixture, no real values
    ".env.schema",
]

for allowed in ALLOWLIST:
    if allowed in path:
        sys.exit(0)

# Block exact filenames and well-known secret file patterns
BLOCKED_EXACT_NAMES = {
    ".env",
    ".netrc",
    "id_rsa",
    "id_ed25519",
    "id_ecdsa",
    "id_dsa",
}

if filename in BLOCKED_EXACT_NAMES:
    print(json.dumps({"reason": f"Blocked: '{raw_path}' is a known secret file. Read via environment variable instead."}))
    sys.exit(2)

# Block files whose name starts with .env followed by a dot or end of string
# Matches: .env, .env.local, .env.production — but not .env.example (caught by allowlist)
if re.match(r"^\.env(\.|$)", filename):
    print(json.dumps({"reason": f"Blocked: '{raw_path}' is an .env file. Use environment variables instead."}))
    sys.exit(2)

# Block credential and key files by extension
BLOCKED_EXTENSIONS = {".pem", ".p12", ".pfx", ".key", ".jks", ".keystore", ".cer", ".crt"}
if Path(filename).suffix in BLOCKED_EXTENSIONS:
    print(json.dumps({"reason": f"Blocked: '{raw_path}' has a credential file extension. Reference via environment variable."}))
    sys.exit(2)

# Block well-known credential paths (not just filename)
BLOCKED_PATH_SEGMENTS = [
    ".aws/credentials",
    ".aws/config",
    ".ssh/",
    "client_secret.json",       # Google OAuth desktop credential file
    "service_account.json",     # GCP service account key
    "firebase_adminsdk",
]

for segment in BLOCKED_PATH_SEGMENTS:
    if segment in path:
        print(json.dumps({"reason": f"Blocked: '{raw_path}' matches a known credential path pattern."}))
        sys.exit(2)

sys.exit(0)
