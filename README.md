# BidKit

**제안서, 이제 AI 에이전트 팀이 같이 씁니다.**

탑티어 수준의 기술 제안서를 전략 수립부터 최종 출력까지, 5개 전문 에이전트가 분업하여 작성하는 Claude Code 플러그인입니다.

---

## 시작하기

### 1. Claude Code 설치

터미널(맥: Terminal, 윈도우: PowerShell)을 열고 아래를 복사해서 붙여넣으세요.

```bash
npm install -g @anthropic-ai/claude-code
```

> Node.js가 없다면 먼저 https://nodejs.org 에서 LTS 버전을 설치하세요.

### 2. Claude Code 실행

```bash
claude
```

처음 실행하면 Anthropic 로그인 화면이 뜹니다. 안내에 따라 로그인하세요.

### 3. BidKit 플러그인 설치

Claude Code 안에서 아래 두 줄을 순서대로 입력하세요:

```
/plugin marketplace add DinN0000/bid-marketplace
/plugin install bid
```

### 4. 업데이트

이력 재작성으로 인해 기존 설치에서 업데이트 충돌이 날 수 있습니다.
문제가 생기면 마켓플레이스를 삭제 후 재추가하세요:

```
/plugin marketplace remove DinN0000/bid-marketplace
/plugin marketplace add DinN0000/bid-marketplace
/plugin install bid
```

자동 업데이트를 켜두면 이후부터는 세션 시작 시 자동 반영됩니다:
플러그인 TUI → Marketplaces 탭 → DinN0000/bid-marketplace → Auto-update ON

### 5. 사용하기

설치가 끝나면 그대로 말하면 됩니다:

```
"RFP 받았는데 제안서 만들어야 해"
```

BidKit이 전략 수립부터 시작합니다.

### 6. 문서 파서 (선택)

RFP가 PDF라면 바로 읽습니다. PPTX/DOCX/XLSX 파일도 읽으려면:

```bash
uv pip install -r parser/requirements.txt --system
```

지금 안 해도 됩니다. 필요할 때 BidKit이 안내해줍니다.

---

## How It Works

### 팀 구조

```
                     ┌───────────┐
                     │ Overseer  │  전략, 교차검증, 최종승인
                     └─────┬─────┘
          ┌────────┬───────┼───────┬────────┐
          ▼        ▼       ▼       ▼        ▼
       ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐  .bidkit/meta/
       │  BA  │ │  DA  │ │  TA  │ │  SA  │  outline, glossary
       │  Team│ │  Team│ │  Team│ │  Team│  rfp-trace-matrix
       └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘
          ▼        ▼        ▼        ▼
       ssot/ba/    da/    ta/    sa/
```

| Team | 산출물 | 핵심 규칙 |
|------|--------|---------|
| **BA** | 사업 개요, 요구사항, 업무 프로세스 | 모든 기능 = 흐름도 + 화면 |
| **DA** | 데이터 모델, 마이그레이션, 보안 | 5-Part 순서, PK/FK 필수, 암호화 기준 |
| **TA** | 아키텍처, H/W-S/W 구성, 이행, 비용 | 3환경 분리, H/W 수량 = 비용표 |
| **SA** | 솔루션 스펙, 비교표, 레퍼런스, 라이선스 | 5-Part 구조, 성능 = 측정조건 포함 |

### 작업 프로세스

각 팀 안에서 4명이 릴레이로 움직입니다.

```
① Team Lead: SSOT 상태 읽고 모드 감지
        │
② Researcher: 자료 수집 (스펙, 레퍼런스, RFP)
        │
③ Writer: 초안 작성 (도메인 패턴 적용)
        │
   ┌───────────────────────────────┐
   │ ④ Critic: 검증                 │
   │    품질 기준 + RFP 대조         │
   │         │                     │
   │     FAIL │    PASS            │
   │         ▼      │             │
   │ ⑤ Writer: 수정  │             │  ◀── PASS 날 때까지 반복
   │         └──▶ ④ 재검증          │
   └───────────────────────────────┘
                    │ PASS
⑥ Team Lead: 사용자에게 제시 → User Confirm
                    │
⑦ Overseer: 교차 검토 (용어, 수치, 의존성)
              │            │
          Directive     Confirmed ✓
              └──▶ Writer 수정 ──▶ Critic 재검증
```

이런 걸 잡아줍니다:

```
✗ "HSM 장비" vs "HSM 서버" ─── 용어 통일
✗ 아키텍처 10대 vs 비용표 8대 ─ 수치 검증
✗ RFP 3.2.1항 미반영 ──────── 누락 탐지
✗ 망분리 기준 미충족 ──────── 규정 검증
```

---

## Usage

명령어를 외울 필요 없습니다. 자연어로 말하면 자동 라우팅됩니다.

```
"HSM 모델 변경해야 해"           →  해당 섹션 자동으로 열고 수정
"전체적으로 좀 약한 것 같아"       →  전 섹션 품질 진단 + 개선 우선순위
"교차 검증해줘"                   →  숫자 · 용어 · 수량 일관성 체크
"진행 상황 알려줘"                →  팀별 진행률 + 다음 할 일 안내
"PDF로 출력해줘"                  →  확정 섹션만 모아서 렌더링
```

명령어를 쓰고 싶다면:

| Command | Purpose |
|---------|---------|
| `/bid:design` | 전략 수립 + 목차 생성 |
| `/bid:write <section>` | 섹션 작성/수정 |
| `/bid:diagnose` | 품질 진단 + 교차 검증 |
| `/bid:status` | 진행 현황 |
| `/bid:setup` | 환경 점검 |

---

## Key Features

### SSOT-Based Section Management

모든 섹션은 독립된 SSOT (Single Source of Truth) 문서로 관리됩니다.

```
ideation → draft → verifying → verified → tentative → reviewing → confirmed ✓
```

### Impact Analysis

확정된 섹션을 수정하면, 영향받는 다른 섹션을 자동으로 파악하고 알려줍니다.

---

## Platform Support

| Platform | Entry Point | Interface |
|----------|-------------|-----------|
| **Claude Code** | `CLAUDE.md` | `/bid:` commands or natural language |
| **Codex** | `AGENTS.md` | Natural language |

---

## License

MIT
