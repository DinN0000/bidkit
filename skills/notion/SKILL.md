# /notion — Upload Proposal to Notion

## Trigger

Command: `/bid:notion`
Natural language: "노션에 올려줘", "팀 리뷰용으로 공유해줘", "노션에 업데이트해줘"

---

## Prerequisites

This skill requires one of the following Notion integrations:

1. **Notion MCP Server** (recommended): `claude mcp add --transport http notion https://mcp.notion.com/mcp`
2. **notion-cli**: `brew install 4ier/tap/notion-cli`

If neither is available, guide the user through setup:
*"노션 연동이 필요합니다. 아래 중 하나를 선택해주세요:
1. Notion MCP (추천): `claude mcp add --transport http notion https://mcp.notion.com/mcp`
2. notion-cli: `brew install 4ier/tap/notion-cli`"*

---

## Flow

### Step (1) — Detect Integration Method

Check which Notion integration is available:
- If Notion MCP tools are available (e.g., `notion-create-pages`), use MCP mode.
- If `notion-cli` is installed (check via `which notion-cli`), use CLI mode.
- If both are available, prefer MCP mode.

### Step (2) — Determine Upload Scope

Ask the user what to upload:

| User Intent | Action |
|-------------|--------|
| "전체 올려줘" | Upload all confirmed/tentative SSOTs |
| "HSM 섹션 올려줘" | Upload specific SSOT |
| "최종본 올려줘" | Run output assembly first, then upload unified document |
| No specification | Default to all confirmed SSOTs |

### Step (3) — Collect Target SSOTs

Scan `proposal/ssot/<team>/` and filter by status:

| Status | Action |
|--------|--------|
| `confirmed` | Upload |
| `tentative` | Upload with `[TENTATIVE]` marker |
| `verified` | Upload with `[PENDING REVIEW]` marker |
| `draft` / `verifying` | Skip; inform user |
| `ideation` | Skip |

### Step (4) — Upload to Notion

#### MCP Mode

For each SSOT to upload:
1. Search Notion for existing page with matching title.
2. If found, update the existing page content.
3. If not found, create a new page under the target database/page.
4. Set page properties: status, team, last updated.

For unified output:
1. Read `proposal/output/proposal-vN.md` (latest version).
2. Create or update a single Notion page with the full assembled content.

#### CLI Mode

For each SSOT to upload:
```bash
# Create new page
notion-cli page create --parent <DB_ID> --title "<section-title>" --body <ssot-file>

# Update existing page
notion-cli block append <PAGE_ID> --file <ssot-file>
```

For unified output:
```bash
notion-cli page create --parent <DB_ID> --title "Proposal v<N>" --body proposal/output/proposal-vN.md
```

### Step (5) — Report Results

Report upload summary:
```
노션 업로드 완료:
  ✅ sa-hsm-001 — HSM 솔루션 (confirmed)
  ✅ ta-infra-001 — 인프라 아키텍처 (confirmed)
  ⚠️ ba-overview-001 — 사업 개요 (tentative)
  ⏭️ da-model-001 — 데이터 모델 (draft, 건너뜀)

노션에서 팀원들이 댓글로 리뷰할 수 있습니다.
```

### Step (6) — First-Time Setup

On first use, ask the user for the Notion target:
*"노션 어디에 올릴까요? 페이지 URL이나 데이터베이스 URL을 알려주세요."*

Save the target to `proposal/.bidkit/runtime/notion-config.json`:
```json
{
  "target_type": "database",
  "target_id": "<database-or-page-id>",
  "integration": "mcp",
  "last_upload": ""
}
```

On subsequent uses, reuse the saved target. If the user wants to change it:
*"다른 곳에 올릴까요? 새 URL을 알려주세요."*

---

## Proposal Guide

**Render at the bottom of every response** per `reference/proposal-guide-format.md`.
