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
MMDC=$(check command -v mmdc)
NOTION_CLI=$(check command -v notion-cli)

# Notion MCP: check if registered in claude mcp list
if command -v claude >/dev/null 2>&1 && claude mcp list 2>/dev/null | grep -q "notion"; then
  NOTION_MCP="true"
else
  NOTION_MCP="false"
fi

cat <<EOF
{
  "required": {
    "git": $GIT
  },
  "tools": {
    "uv": $UV
  },
  "output": {
    "pandoc": $PANDOC,
    "mermaid-cli": $MMDC
  },
  "parsing": {
    "bidkit-parser": $PARSER,
    "node": $NODE
  },
  "notion": {
    "notion-mcp": $NOTION_MCP,
    "notion-cli": $NOTION_CLI
  }
}
EOF
