# Changelog

## [1.0.0] - 2026-03-15

### BidKit 1.0 Release

프로젝트명 변경: Proposal Harness → **BidKit**

### Added

- **Plugin packaging** — Claude Code 플러그인 (`bid`)으로 패키징
  - `.claude-plugin/plugin.json` 매니페스트
  - `/bid:design`, `/bid:write`, `/bid:diagnose`, `/bid:status`, `/bid:setup` 명령어
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
