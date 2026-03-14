#!/bin/bash
# Dependency detection for BidKit
# Outputs JSON with required/optional tool availability

check() {
  if "$@" >/dev/null 2>&1; then echo "true"; else echo "false"; fi
}

GIT=$(check command -v git)
UV=$(check command -v uv)
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PARSER=$(check test -f "$SCRIPT_DIR/parser/__init__.py")
PANDOC=$(check command -v pandoc)
NODE=$(check command -v node)

cat <<EOF
{
  "required": {
    "git": $GIT
  },
  "tools": {
    "uv": $UV
  },
  "optional": {
    "bidkit-parser": $PARSER,
    "pandoc": $PANDOC,
    "node": $NODE
  }
}
EOF
