# BidKit

**금융 IT 제안서, 이제 AI 에이전트 팀이 같이 씁니다.**

RFP 던지면 전략부터 잡고, 섹션별로 나눠서 작성하고, 교차 검증까지 — 탑티어 수준의 기술 제안서를 만들어내는 Claude Code 플러그인입니다.

---

## 왜 BidKit인가

제안서 PM이라면 공감할 겁니다:

- HSM 스펙 바뀌면 비용표도 바꿔야 하고, 이행계획도 바꿔야 하고...
- "이 숫자 아까 그 섹션이랑 맞아?" 교차 확인에 반나절
- 30명이 쓴 문서의 용어가 제각각
- 마감 3일 전에 RFP 보완공고

BidKit은 이런 문제를 **5개 전문 에이전트가 협업하는 구조**로 해결합니다:

| 누가 | 뭘 하는가 |
|------|-----------|
| **Overseer** | 전체 전략 수립, 섹션 간 일관성 검증, 최종 승인 |
| **Team Lead** | BA/DA/TA/SA 도메인별 작업 조율 |
| **Writer** | 제안서 본문 작성 (정확한 스펙, 정량적 근거) |
| **Researcher** | 제품 스펙, 인증, 레퍼런스, 경쟁사 분석 수집 |
| **Critic** | RFP 요구사항 커버리지, 수치 정합성, 규정 준수 검증 |

모든 섹션은 작성 → 검증 → 수정 → 사용자 확인 → 최종 승인의 5단계를 거칩니다.
**사용자가 승인하지 않으면 어떤 내용도 확정되지 않습니다.**

---

## 30초 시작

```bash
# Claude Code에서 플러그인 로드
claude --plugin-dir /path/to/bidkit
```

그다음, 말만 하면 됩니다:

```
"RFP 받았는데 제안서 만들어야 해"
```

BidKit이 알아서 전략 수립부터 시작합니다. 명령어를 외울 필요 없습니다.

---

## 이런 것도 됩니다

```
"HSM 모델 변경해야 해"           →  해당 섹션 자동으로 열고 수정 시작
"전체적으로 좀 약한 것 같아"       →  전 섹션 품질 진단 + 개선 우선순위 제시
"교차 검증해줘"                   →  숫자, 용어, 서버 수량 일관성 자동 체크
"진행 상황 알려줘"                →  팀별 진행률 + 다음 할 일 안내
"PDF로 출력해줘"                  →  확정된 섹션만 모아서 출력
```

명령어를 쓰고 싶다면:

| 명령어 | 용도 |
|--------|------|
| `/bid:design` | 전략 수립 + 목차 생성 |
| `/bid:write <section>` | 섹션 작성/수정 |
| `/bid:diagnose` | 전체 품질 진단 |
| `/bid:verify` | 교차 검증 |
| `/bid:status` | 진행 현황 |
| `/bid:setup` | 환경 점검 |

---

## 핵심 기능

### SSOT 기반 섹션 관리

모든 섹션은 독립된 SSOT (Single Source of Truth) 문서입니다. 각 섹션은 자체 상태 머신을 가지고 있어서 누가 무엇을 어디까지 했는지 항상 추적됩니다.

```
ideation → draft → verifying → verified → tentative → reviewing → confirmed
```

### 교차 검증

서버 수량이 아키텍처 섹션에서는 10대인데 비용표에서는 8대? BidKit이 자동으로 찾아냅니다.

- 용어 일관성 (같은 서버를 다른 이름으로 부르고 있지 않은지)
- 수치 정합성 (서버 수, 비용, TPS가 섹션 간 일치하는지)
- RFP 요구사항 커버리지 (빠뜨린 요구사항이 없는지)
- 규정 준수 (금융보안원 가이드라인, 망분리 등)

### 영향도 분석

확정된 섹션을 수정하면, 영향받는 다른 섹션을 자동으로 파악하고 알려줍니다.

### RFP 문서 파싱

PDF는 바로 읽고, PPTX/DOCX/XLSX는 parser 설치 후 읽습니다:

```bash
pip install bidkit-parser
```

필요한 시점에 BidKit이 자동으로 안내하니, 미리 설치하지 않아도 됩니다.

---

## Agent Architecture

```
Overseer (EA)
├── BA Team (사업분석)
│   └── Team Lead → Writer, Researcher, Critic
├── DA Team (데이터아키텍처)
│   └── Team Lead → Writer, Researcher, Critic
├── TA Team (기술아키텍처)
│   └── Team Lead → Writer, Researcher, Critic
└── SA Team (솔루션아키텍처)
    └── Team Lead → Writer, Researcher, Critic
```

독립적인 섹션은 **병렬로 작업**됩니다. 사용자와의 대화는 순차적으로, 백그라운드 작업은 동시에.

---

## Platform Support

| 플랫폼 | 엔트리포인트 | 사용법 |
|--------|-------------|--------|
| **Claude Code** | `CLAUDE.md` | `/bid:` 명령어 또는 자연어 |
| **Codex** | `AGENTS.md` | 자연어 |

---

## License

MIT
