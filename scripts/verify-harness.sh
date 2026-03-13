#!/bin/bash

# Harness Integrity Validation Script
# Validates the presence of all required files in the harness structure

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Counters
PASS=0
FAIL=0

# Helper function to check if a file exists
check_file() {
  local filepath="$1"
  if [ -f "$filepath" ]; then
    echo -e "${GREEN}✓${NC} $filepath"
    ((PASS++))
    return 0
  else
    echo -e "${RED}✗${NC} $filepath"
    ((FAIL++))
    return 1
  fi
}

# Helper function to check if a file contains a required string
check_contains() {
  local filepath="$1"
  local pattern="$2"
  local description="$3"

  if grep -q "$pattern" "$filepath"; then
    echo -e "${GREEN}✓${NC} $description"
    ((PASS++))
    return 0
  else
    echo -e "${RED}✗${NC} $description"
    ((FAIL++))
    return 1
  fi
}

# Get the root directory (parent of scripts directory)
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "=========================================="
echo "Harness Integrity Validation"
echo "=========================================="
echo ""

# Check core documentation files
echo "Core Documentation:"
check_file "AGENTS.md"
check_file "CLAUDE.md"
check_file "ARCHITECTURE.md"
echo ""

# Check agent documentation
echo "Agents:"
check_file "agents/overseer.md"
check_file "agents/team-lead.md"
check_file "agents/writer.md"
check_file "agents/researcher.md"
check_file "agents/critic.md"
echo ""

# Check skills documentation
echo "Skills:"
check_file "skills/design.md"
check_file "skills/write.md"
check_file "skills/diagnose.md"
check_file "skills/verify.md"
check_file "skills/status.md"
check_file "skills/output.md"
echo ""

# Check templates
echo "Templates:"
check_file "templates/ssot.md"
check_file "templates/ideation-note.md"
check_file "templates/init/proposal-meta.yaml"
check_file "templates/init/glossary.yaml"
check_file "templates/init/outline.yaml"
check_file "templates/init/rfp-trace-matrix.md"
echo ""

# Check reference documentation
echo "Reference:"
check_file "reference/state-machine.md"
check_file "reference/quality-criteria.md"
check_file "reference/proposal-guide-format.md"
check_file "reference/impact-rules.md"
check_file "reference/skills-catalog.md"
check_file "reference/cross-team-communication.md"
check_file "reference/error-handling.md"
echo ""

# Check entrypoint files for key path references
echo "=========================================="
echo "Entrypoint Content Validation"
echo "=========================================="
for entry_file in AGENTS.md CLAUDE.md; do
  if [ -f "$entry_file" ]; then
    echo "Checking for key path references in $entry_file..."
    check_contains "$entry_file" "agents/" "$entry_file references agents/"
    check_contains "$entry_file" "skills/" "$entry_file references skills/"
    check_contains "$entry_file" "reference/" "$entry_file references reference/"
  else
    echo -e "${RED}✗${NC} $entry_file not found"
    ((FAIL++))
  fi
done
echo ""

# SSOT Template Structure Check
echo "=========================================="
echo "SSOT Template Structure Validation"
echo "=========================================="
SSOT_TEMPLATE="templates/ssot.md"
if [ -f "$SSOT_TEMPLATE" ]; then
  echo "Checking $SSOT_TEMPLATE for required structure..."
  # YAML frontmatter markers
  check_contains "$SSOT_TEMPLATE" "^---" "$SSOT_TEMPLATE contains YAML frontmatter markers (---)"
  # Required frontmatter fields
  check_contains "$SSOT_TEMPLATE" "^id:" "$SSOT_TEMPLATE contains frontmatter field: id"
  check_contains "$SSOT_TEMPLATE" "^title:" "$SSOT_TEMPLATE contains frontmatter field: title"
  check_contains "$SSOT_TEMPLATE" "^team:" "$SSOT_TEMPLATE contains frontmatter field: team"
  check_contains "$SSOT_TEMPLATE" "^status:" "$SSOT_TEMPLATE contains frontmatter field: status"
  check_contains "$SSOT_TEMPLATE" "^version:" "$SSOT_TEMPLATE contains frontmatter field: version"
  # Required body sections
  check_contains "$SSOT_TEMPLATE" "## Summary" "$SSOT_TEMPLATE contains section: ## Summary"
  check_contains "$SSOT_TEMPLATE" "## Content" "$SSOT_TEMPLATE contains section: ## Content"
  check_contains "$SSOT_TEMPLATE" "## Supporting Evidence" "$SSOT_TEMPLATE contains section: ## Supporting Evidence"
  check_contains "$SSOT_TEMPLATE" "## Verification Log" "$SSOT_TEMPLATE contains section: ## Verification Log"
  check_contains "$SSOT_TEMPLATE" "## Overseer Review Log" "$SSOT_TEMPLATE contains section: ## Overseer Review Log"
else
  echo -e "${RED}✗${NC} $SSOT_TEMPLATE not found — skipping template checks"
  ((FAIL++))
fi
echo ""

# State Machine Consistency Check
echo "=========================================="
echo "State Machine Consistency"
echo "=========================================="
STATE_FILE="reference/state-machine.md"
if [ -f "$STATE_FILE" ]; then
  echo "Checking $STATE_FILE for all valid states..."
  check_contains "$STATE_FILE" "ideation" "$STATE_FILE contains state: ideation"
  check_contains "$STATE_FILE" "draft" "$STATE_FILE contains state: draft"
  check_contains "$STATE_FILE" "verifying" "$STATE_FILE contains state: verifying"
  check_contains "$STATE_FILE" "verified" "$STATE_FILE contains state: verified"
  check_contains "$STATE_FILE" "tentative" "$STATE_FILE contains state: tentative"
  check_contains "$STATE_FILE" "reviewing" "$STATE_FILE contains state: reviewing"
  check_contains "$STATE_FILE" "confirmed" "$STATE_FILE contains state: confirmed"
  check_contains "$STATE_FILE" "revision" "$STATE_FILE contains state: revision"
else
  echo -e "${RED}✗${NC} $STATE_FILE not found — skipping state machine checks"
  ((FAIL++))
fi
echo ""

# Cross-Entrypoint Sync Check
echo "=========================================="
echo "Cross-Entrypoint Sync (CLAUDE.md vs AGENTS.md)"
echo "=========================================="
if [ -f "CLAUDE.md" ] && [ -f "AGENTS.md" ]; then
  SYNC_OK=true
  CLAUDE_CONTENT=$(cat CLAUDE.md)
  AGENTS_CONTENT=$(cat AGENTS.md)

  for ref_file in agents/overseer.md agents/team-lead.md agents/writer.md agents/researcher.md agents/critic.md skills/design.md skills/write.md skills/diagnose.md skills/verify.md skills/status.md skills/output.md; do
    CLAUDE_HAS=$(grep -c "$ref_file" <<< "$CLAUDE_CONTENT" || true)
    AGENTS_HAS=$(grep -c "$ref_file" <<< "$AGENTS_CONTENT" || true)
    if [ "$CLAUDE_HAS" -gt 0 ] && [ "$AGENTS_HAS" -gt 0 ]; then
      echo -e "${GREEN}✓${NC} Both entrypoints reference $ref_file"
      ((PASS++))
    else
      echo -e "${RED}✗${NC} Mismatch: $ref_file (CLAUDE.md: $CLAUDE_HAS, AGENTS.md: $AGENTS_HAS)"
      ((FAIL++))
      SYNC_OK=false
    fi
  done

  if [ "$SYNC_OK" = true ]; then
    echo -e "${GREEN}Entrypoints are in sync.${NC}"
  else
    echo -e "${RED}Entrypoints have mismatched references.${NC}"
  fi
else
  echo -e "${RED}✗${NC} One or both entrypoints missing — skipping sync check"
  ((FAIL++))
fi
echo ""

# Print summary
TOTAL=$((PASS + FAIL))
echo "=========================================="
echo "Summary: $PASS/$TOTAL checks passed"
echo "=========================================="
if [ $FAIL -eq 0 ]; then
  echo -e "${GREEN}All checks passed!${NC}"
  exit 0
else
  echo -e "${RED}$FAIL checks failed${NC}"
  exit 1
fi
