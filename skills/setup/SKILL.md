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
- Group by: 필수 → 출력 → 파싱 → 노션 연동
- End with a reassurance that most features work without optional tools

## Example Output

환경 점검 결과:

[필수]
✅ git — 버전 관리

[선택 — 출력]
❌ pandoc — PDF 출력
   설치: brew install pandoc (macOS) / apt install pandoc (Linux)
❌ mermaid-cli — 다이어그램 이미지 변환 (PPT용)
   설치: npm install -g @mermaid-js/mermaid-cli

[선택 — 파싱]
❌ bidkit-parser — PPTX/DOCX/XLSX 파싱
   설치: uv pip install -r parser/requirements.txt --system
✅ node — 고급 계약 검증

[선택 — 노션 연동]
❌ Notion MCP — 노션 업로드 (추천)
   설치: claude mcp add --transport http notion https://mcp.notion.com/mcp
❌ notion-cli — 노션 업로드 (대안)
   설치: brew install 4ier/tap/notion-cli

필요한 것만 설치하시면 됩니다.
선택 항목 없이도 Markdown 기반 제안서 작성은 모두 가능합니다.

## After Check

Show the Proposal Guide footer with:
Recommended: /bid:design — 새 제안서 프로젝트를 시작합니다
