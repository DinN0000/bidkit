# Changelog

## [1.1.0] - 2026-06-12

### "모든 문서는 결국 제안이다" — Doctype 확장 + 개조식 품질 체계

### Added

- **Doctype 프로필** (`reference/doctypes/`) — 제안 우산 아래 3개 문서 타입
  - `proposal` — B2B 제안서 (회사 → 발주사, RFP 기준, win strategy)
  - `portfolio` — 포트폴리오 (개인 → 회사, JD·공고 기준, 포지셔닝 전략)
  - `business-report` — 사업/경영 보고 (팀 → 의사결정자, 의사결정 기준, 권고안 채택 전략 + Lite Loop)
  - `/bid:design` Step 0에서 doctype 결정, 메타에 `doctype`/`audience`/`decision_requested` 기록
  - 범용 기준 추적: `templates/init/criteria-trace-matrix.md` (RFP가 없는 doctype용)
  - Key Rule 10: 모든 에이전트는 작업 전 doctype 프로필을 읽음
- **개조식 스타일 가이드** (`reference/style-guide.md`) — 명사형 종결, 억지 강조 금지
  ("핵심은", "가장 중요한 것은"), 접속사·완곡 표현 금지, Before/After 변환 예시
- **Single-home 중복 방지** — 한 정보는 한 곳에만, 타 섹션은 `[REF: id]` 참조
  - SSOT frontmatter `scope`/`not_in_scope` 필드 (MECE 경계를 설계 단계에서 확정)
  - Critic 체크리스트 7 (Style Compliance), 8 (Internal Redundancy) 신설 — Warning = FAIL
- **통합본 전체 검토 게이트** — 출력 파이프라인 Step (7): 렌더링 전에 Overseer가
  조립본 전체를 읽고 전역 중복·문체 균일성·흐름 검증 (`playbooks/output/SKILL.md`)
- **Key Rule 9** — 선택지는 설명 대신 ASCII 예시/미리보기로 제시

### Changed

- Writer 문체 지침: 합쇼체 → 개조식 (`reference/style-guide.md` 단일 기준)
- diagnose 중복 검출 심각도: Info → Warning (canonical 소유 지정 + 참조화 액션)
- Critic 체크 1 (RFP coverage → Audience Criteria Coverage), 6 (Regulatory)을
  doctype 조건부로 일반화
- `validate-bidkit-contracts.js`: Proposal Guide "Current 줄" 검사를 현재 문서
  포맷에 맞게 수정 (구버전 리터럴 → 정규식)

## [1.0.0] - 2026-03-15

### BidKit 1.0 Release

프로젝트명 변경: Proposal Harness → **BidKit**

### Added

- **Plugin packaging** — Claude Code 플러그인 (`bid`)으로 패키징
  - `.claude-plugin/plugin.json` 매니페스트
  - `/bid:design`, `/bid:write`, `/bid:status`, `/bid:setup`, `/bid:notion` 명령어
  - 자연어 전용: 진단 ("교차 검증해줘"), 출력 ("PDF로 출력해줘")
  - 스킬 폴더 구조 (`skills/*/SKILL.md`)
- **Dependency detection** — `scripts/check-deps.sh`로 환경 자동 감지
  - 각 스킬에서 필요한 도구가 없으면 설치 안내
  - `/bid:setup`으로 전체 환경 한 번에 점검
- **Document parser** — PDF/DOCX/PPTX/XLSX 문서 파싱 모듈
  - [daekeun-ml/doc-parser](https://github.com/daekeun-ml/doc-parser)에서 추출 코드 포팅
  - AWS Bedrock 의존성 완전 제거
  - Docling 기반 PDF 추출 (테이블 구조, 이미지 분류)
  - python-docx/pptx/openpyxl 기반 Office 파싱
  - 별도 pip 패키지 (`bidkit-parser`)로 분리
- **Codex compatibility** — `AGENTS.md` 엔트리포인트로 Codex 지원
  - 자연어 기반 Recommended 형식
  - 플랫폼별 Proposal Guide 분기
- **Proposal Guide** — 매 응답 하단에 현황 + 추천 명령어 + 설명 표시

### Core System (from initial development)

- **5-agent architecture** — Overseer, Team Lead, Writer, Researcher, Critic
- **SSOT-centric workflow** — 모든 콘텐츠를 SSOT 문서로 관리
- **Session loop** — Generate → Verify → Revise → User Confirm → Overseer Review
- **State machine** — ideation → draft → verifying → verified → tentative → reviewing → confirmed
- **Natural language routing** — 한국어/영어 자연어 입력 자동 라우팅
- **6 skills** — design, write, diagnose, verify, status, output
- **Quality criteria** — 도메인별 품질 기준 (제품스펙, 아키텍처, 비용, 구현계획 등)
- **Impact propagation** — 확정 SSOT 수정 시 영향도 자동 분석
- **Cross-team communication** — 팀 간 의존성 알림, 용어 동기화, 에스컬레이션 프로토콜
- **Validation** — `scripts/verify-bidkit.sh` (77 checks), `scripts/validate-bidkit-contracts.js`
- **Eval fixtures** — design, write, verify 회귀 테스트 프롬프트

### Hardening

- Runtime state를 optional/advisory로 명시 (SSOT fallback)
- `required_for_output` 미지정 시 `true` 기본값
- Node.js 없이도 검증 스크립트 동작 (graceful skip)
- Contract validator에 파일 읽기 캐시 추가
