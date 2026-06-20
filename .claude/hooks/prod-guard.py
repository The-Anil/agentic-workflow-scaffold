#!/usr/bin/env python3
"""
Hook: prod-guard
Event: PreToolUse (Bash)
Blocks commands that deploy or push to production environments.
Context-aware: allows dev/local registry pushes, blocks production ones.

NOTE: This is a nudge, not a security boundary. A determined user can bypass
it by rephrasing. Its value is preventing accidental production deploys, not
malicious ones. Do not rely on this as your only production safeguard.
Exit 2 = blocked. Exit 0 = allowed.
"""
import sys
import json
import re

data = json.load(sys.stdin)
cmd = data.get("tool_input", {}).get("command", "").strip()
cmd_lower = cmd.lower()

# --- Always-block patterns (no context check needed) ---
UNCONDITIONAL_BLOCKS = [
    # Explicit production env flags
    (r"\bnode_env=production\b", "NODE_ENV=production detected"),
    (r"\bnpm run prod\b", "npm run prod detected"),
    (r"\byarn prod\b", "yarn prod detected"),
    (r"--production\b", "--production flag detected"),

    # Deployment CLIs pointing to production
    (r"\bfly deploy\b", "Fly.io deploy detected"),
    (r"\bvercel\s+--prod\b", "Vercel --prod deploy detected"),
    (r"\bheroku push\s+(main|master)\b", "Heroku production push detected"),
    (r"\brailway up\s+--prod\b", "Railway production deploy detected"),
    (r"\bgcloud app deploy\b", "GCP App Engine deploy detected"),
    (r"\bkubectl apply.+--namespace=prod\b", "kubectl prod namespace detected"),
    (r"\bkubectl apply.+namespace prod\b", "kubectl prod namespace detected"),
    (r"\baws elasticbeanstalk.+deploy\b", "Elastic Beanstalk deploy detected"),
]

for pattern, reason in UNCONDITIONAL_BLOCKS:
    if re.search(pattern, cmd_lower):
        print(json.dumps({
            "reason": (
                f"Blocked: {reason}. "
                "Confirm production deployment with the user first. This is a STOP rule."
            )
        }))
        sys.exit(2)

# --- Context-aware docker push ---
# Allow: push to localhost, local registry, dev/staging registries
# Block: push to production-named registries
if "docker push" in cmd_lower:
    allowed_push_patterns = [
        r"localhost[:/]",
        r"127\.0\.0\.1[:/]",
        r"\bdev[./:-]",
        r"\bstaging[./:-]",
        r"\btest[./:-]",
        r"\blocal[:/]",
    ]
    if any(re.search(p, cmd_lower) for p in allowed_push_patterns):
        sys.exit(0)  # dev/local push — allow

    # No dev indicator found — likely production, block and ask
    print(json.dumps({
        "reason": (
            "Blocked: 'docker push' with no dev/local/staging indicator. "
            "If this is a production registry push, confirm with the user first. "
            "If it's a dev registry, add 'localhost:', 'dev.', or 'staging.' to the image tag."
        )
    }))
    sys.exit(2)

sys.exit(0)
