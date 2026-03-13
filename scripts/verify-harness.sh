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

# Get the root directory (parent of scripts directory)
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "=========================================="
echo "Harness Integrity Validation"
echo "=========================================="
echo ""

# Check core documentation files
echo "Core Documentation:"
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

# Check CLAUDE.md for key path references
echo "=========================================="
echo "CLAUDE.md Content Validation"
echo "=========================================="
if [ -f "CLAUDE.md" ]; then
  echo "Checking for key path references in CLAUDE.md..."

  # Check for references to key directories
  if grep -q "agents/" "CLAUDE.md"; then
    echo -e "${GREEN}✓${NC} CLAUDE.md references agents/"
  else
    echo -e "${RED}✗${NC} CLAUDE.md missing reference to agents/"
  fi

  if grep -q "skills/" "CLAUDE.md"; then
    echo -e "${GREEN}✓${NC} CLAUDE.md references skills/"
  else
    echo -e "${RED}✗${NC} CLAUDE.md missing reference to skills/"
  fi

  if grep -q "reference/" "CLAUDE.md"; then
    echo -e "${GREEN}✓${NC} CLAUDE.md references reference/"
  else
    echo -e "${RED}✗${NC} CLAUDE.md missing reference to reference/"
  fi
else
  echo -e "${RED}✗${NC} CLAUDE.md not found"
fi
echo ""

# Print summary
TOTAL=26
echo "=========================================="
echo "Summary: $PASS/$TOTAL files present"
echo "=========================================="
if [ $FAIL -eq 0 ]; then
  echo -e "${GREEN}All required files present!${NC}"
  exit 0
else
  echo -e "${RED}$FAIL files missing${NC}"
  exit 1
fi
