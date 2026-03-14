#!/bin/bash
# Dependency detection for BidKit
# Outputs JSON with required/optional tool availability

check() {
  if "$@" >/dev/null 2>&1; then echo "true"; else echo "false"; fi
}

GIT=$(check command -v git)
PARSER=$(check python3 -c "import harness_parser")
PANDOC=$(check command -v pandoc)
NODE=$(check command -v node)

cat <<EOF
{
  "required": {
    "git": $GIT
  },
  "optional": {
    "harness-parser": $PARSER,
    "pandoc": $PANDOC,
    "node": $NODE
  }
}
EOF
