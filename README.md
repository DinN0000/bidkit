# BidKit

금융 IT 제안서를 멀티에이전트 협업으로 작성하는 Claude Code 플러그인.

100+ 페이지 규모의 기술 제안서를 전략 수립부터 최종 출력까지, 5개 전문 에이전트가 분업하여 작성합니다.

## Quick Start

```bash
# 1. 플러그인 설치
claude --plugin-dir /path/to/bidkit

# 2. 환경 점검 (선택)
/bid:setup

# 3. 제안서 시작
/bid:design
```

또는 자연어로:

```
"RFP 받았는데 제안서 만들어야 해"
```

## Commands

| 명령어 | 용도 |
|--------|------|
| `/bid:design` | 제안서 전략 수립 + 목차 생성 |
| `/bid:write <section>` | 섹션 작성/수정 (모드 자동감지) |
| `/bid:diagnose` | 전체 품질 진단 |
| `/bid:verify` | 교차 검증 (일관성 확인) |
| `/bid:status` | 진행 현황 대시보드 |
| `/bid:setup` | 환경 점검 + 설치 안내 |

자연어 입력도 지원합니다 — 명령어를 몰라도 상황을 설명하면 자동으로 라우팅됩니다.

## Agent Architecture

```
Overseer (EA) — 전략 / 교차검증 / 최종승인
    ├── BA Team Lead (사업분석)
    ├── DA Team Lead (데이터아키텍처)
    ├── TA Team Lead (기술아키텍처)
    └── SA Team Lead (솔루션아키텍처)
        └── 각 팀: Writer + Researcher + Critic
```

| 에이전트 | 역할 |
|---------|------|
| **Overseer** | 전략, 교차 SSOT 일관성, 최종 승인 |
| **Team Lead** | 도메인별 오케스트레이터, 세션 루프 관리 |
| **Writer** | 섹션 콘텐츠 작성/수정 |
| **Researcher** | 스펙, 레퍼런스, 경쟁분석 수집 |
| **Critic** | 품질, 규정 준수, 교차참조 검증 |

## How It Works

모든 제안서 섹션은 **SSOT (Single Source of Truth)** 문서로 관리되며, 5단계 세션 루프를 거칩니다:

```
Generate → Verify → Revise → User Confirm → Overseer Review
```

사용자가 승인하지 않으면 어떤 섹션도 확정되지 않습니다.

## Document Parser (Optional)

PPTX, DOCX, XLSX 형식의 RFP를 읽으려면 parser를 설치하세요:

```bash
pip install bidkit-parser
```

PDF는 Claude Code가 네이티브로 읽으므로 parser 없이도 사용 가능합니다.

필요한 시점에 BidKit이 자동으로 설치를 안내합니다.

## Platform Support

| 플랫폼 | 엔트리포인트 | 명령어 |
|--------|-------------|--------|
| Claude Code | `CLAUDE.md` | `/bid:design` 등 |
| Codex | `AGENTS.md` | 자연어 |

## Project Structure

```
.claude-plugin/           # 플러그인 메타데이터
  plugin.json
agents/                   # 에이전트 역할 정의
  overseer.md
  team-lead.md
  writer.md
  researcher.md
  critic.md
skills/                   # 명령어 구현
  design/SKILL.md
  write/SKILL.md
  diagnose/SKILL.md
  verify/SKILL.md
  status/SKILL.md
  output/SKILL.md
  setup/SKILL.md
templates/                # SSOT 및 출력 템플릿
reference/                # 공유 레퍼런스 (품질기준, 상태머신 등)
parser/                   # 문서 파서 (선택적 확장)
scripts/                  # 검증 스크립트
```

## License

MIT
