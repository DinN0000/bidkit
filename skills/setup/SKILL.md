---
name: setup
description: Check development environment and guide installation of optional tools
---

# Environment Setup Check

Run `bash scripts/check-deps.sh` and present the results.

## Output Format

Present results as a checklist with installation instructions for missing tools:

- ✅ / ❌ for each tool
- For missing tools, show the install command
- Group by required vs optional
- End with a reassurance that most features work without optional tools

## Example Output

환경 점검 결과:

[필수]
✅ git — 설치됨

[선택]
❌ harness-parser — PPTX/DOCX/XLSX 파싱
   설치: pip install harness-parser
❌ pandoc — PDF 출력
   설치: brew install pandoc (macOS) / apt install pandoc (Linux)
✅ node — 고급 계약 검증

필요한 것만 설치하시면 됩니다.
harness-parser 없이도 PDF RFP는 바로 사용 가능합니다.

## After Check

Show the Proposal Guide footer with:
Recommended: /ph:design — 새 제안서 프로젝트를 시작합니다
