# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **단일 출처 (source of truth)**: 팀 노션 "DB (05.04 14:00 update)" 와 "구조 (05.04 14:30 update)" 가 진짜 결정. 본 문서는 그 결정을 코드 작업 컨텍스트로 옮겨둔 것이다. 노션과 본 문서가 어긋나면 노션이 우선이며, 즉시 본 문서를 갱신해 동기화한다.

---

## 0. 절대규칙 (Hard Rules)

> 아래 항목은 어떤 상황에서도 위반하면 안 된다. 의심스러우면 코드를 작성하기 전에 사용자에게 먼저 확인할 것.

1. **개인정보를 더미데이터에도 사용하지 않는다.**
   - 이용자/활동지원사 더미데이터에 **실명, 실제 주민등록번호, 실제 연락처, 실제 주소**를 절대 넣지 않는다.
   - 시드/픽스처/테스트 데이터는 **명백한 가짜 값**(예: `홍길동`, `010-0000-0001`, `900101-1234567` 같은 형식만 맞춘 더미)만 사용한다.
   - 도메인 특성상 민감정보(장애 등급, 건강 정보, 활동지원급여 정보)가 다수 포함되므로 로그에 PII를 출력하지 않는다.
2. **`plan.md`의 5주 범위 밖 기능을 임의로 추가하지 않는다.**
   - 사용자가 명시적으로 요청하지 않은 기능은 만들지 않는다. 좋은 아이디어라도 먼저 제안하고 승인을 받는다.
   - "있으면 좋을 것 같은" 추가 화면, 추가 필드, 추가 검증 로직은 스코프 크리프이므로 거절한다.
   - 5주 계획 변경이 필요해 보이면 코드 수정 전에 `plan.md`부터 갱신한다.
3. **서류 상태값은 정확히 5종이다**: `미제출 / 제출완료 / 보완필요 / 만료예정 / 만료`. 새 상태를 임의로 추가하지 않는다.
4. **보관기간 5년·점검 2년·만료예정 30일 기준은 매직넘버가 아니라 상수**로 관리한다 (한 곳만 수정하면 전체에 반영되도록).
5. **로그인은 기관 직원(staff)만 가능하다.** 이용자(client)·활동지원사(assistant) 본인 로그인 경로, 공개 회원가입(`/signup`) 같은 엔드포인트를 만들지 않는다. 직원 계정은 관리자가 직접 발급하는 모델이다.
6. **메모는 문서(파일 업로드)와 혼용하지 않는다.**
   - 메모는 `client.client_memo` / `assistant.assistant_memo` 컬럼에 저장한다 (엔티티 단일 텍스트, 덮어쓰기).
   - 문서는 `document` 테이블에 메타데이터로, 실제 파일은 파일시스템에 저장한다.
   - 화일 화면에서는 "서류" 탭과 "메모" 탭을 분리한다. 한쪽 데이터를 다른 쪽 모델에 섞어 저장하지 않는다.

---

## 1. 아키텍처 (Architecture)

### 기술 스택
| 레이어 | 기술 |
| --- | --- |
| Frontend | **React + TypeScript + Vite** |
| Backend | **Python + FastAPI** |
| Database | **MySQL / MariaDB** |
| ORM | SQLAlchemy + Alembic 마이그레이션 |
| 인증 | JWT 기반 세션 (`organization_id` 클레임 포함) |
| 파일 저장 | 로컬 파일시스템 (MVP), 메타데이터만 DB |

### 폴더 구조 (현재 코드 기준)

```
helper-hub/
├── plan.md              # 5주 계획 (단일 출처)
├── CLAUDE.md            # 이 파일
├── frontend/            # React + Vite
│   ├── src/
│   │   ├── pages/       # 화면 단위 (대시보드, 이용자, 활동지원사, 화일, 이용내역…)
│   │   ├── components/  # 공용 UI
│   │   ├── api/         # FastAPI 호출 래퍼
│   │   ├── types/       # 도메인 타입 (Client, Assistant, Document…)
│   │   └── lib/         # 상수 (서류 상태, 보관기간 등)
│   └── package.json
└── backend/             # FastAPI
    ├── app/
    │   ├── main.py
    │   ├── api/
    │   │   ├── api.py         # 메인 /api 라우터 (모든 도메인 라우터 통합)
    │   │   ├── deps.py        # get_current_staff 등 인증 의존성
    │   │   └── routers/       # 도메인별 라우터 (auth, client, assistant, document, assignment …)
    │   ├── core/              # ⚠ 단일 파일이 아니라 셋으로 분리되어 있다
    │   │   ├── config.py      # pydantic-settings 환경변수 매핑
    │   │   ├── database.py    # SQLAlchemy engine / SessionLocal / Base / get_db
    │   │   └── security.py    # bcrypt 해시·검증, JWT 인코드/디코드
    │   ├── models/            # SQLAlchemy (organization, staff, client, assistant, assignment, service_log, document, document_requirement)
    │   ├── schemas/           # Pydantic 스키마 (auth_schema, client_schema, assistant_schema, document_schema, assignment_schema)
    │   └── services/          # 비즈니스 로직 (근속 계산, 2년 필터, 매칭, organization 격리 …)
    ├── scripts/               # 시드/일회성 스크립트
    ├── alembic/
    └── pyproject.toml
```

### 데이터 흐름 핵심

- **멀티 테넌시**: `organization` 테이블이 시스템 루트. `staff` / `client` / `assistant` / `document` 모두 `organization_id` FK 보유.
  - JWT 페이로드에 `sub` (staff_id) 와 **`organization_id`** 클레임을 포함한다 (`backend/app/core/security.py::create_access_token`).
  - 인증 의존성(`backend/app/api/deps.py::get_current_staff`)은 토큰의 `organization_id` 와 DB staff 의 `organization_id` 가 일치하는지 검증해 다른 기관 데이터로의 횡단 접근을 차단한다.
  - 모든 `/api/*` 라우트는 인증 staff 의 organization 범위 내 데이터만 조회/변경한다 (애플리케이션 레벨 강제 — 누락하면 데이터 누출).
- **3대 화일** (기관/이용자/활동지원사) 은 별도 테이블이 아니라 `document` 테이블 단일.
  - 어떤 엔티티에 속한 문서인지는 `document.requirement_id` → `document_requirement.target_type` (`'client'` | `'assistant'` 등) 로 결정.
  - 분류(예: "기본서류", "이력서") 도 `document_requirement.document_name` 에 정의되어 있다.
- **메모**는 별도 테이블(`notes`)이 아니라 각 엔티티의 단일 텍스트 컬럼:
  - `client.client_memo`, `assistant.assistant_memo` — 엔티티당 1건, 덮어쓰기.
  - `document.document_memo` — 문서별 첨부 메모.
  - 시계열 누적 메모는 5주 범위 밖이므로 만들지 않는다.
- **이용자 ↔ 활동지원사**는 `assignment` 테이블로 N:M 관리. 매칭 기준은 이용자 욕구(텍스트) ↔ 활동지원사 근무 가능 요일/시간(`assistant.work_days`).
- **2년치 점검 대비 뷰**는 별도 테이블이 아니라 `created_date >= NOW() - INTERVAL 2 YEAR` 필터로 구현 (서비스 레이어).
- **근속기간**은 저장하지 않고 `assistant.work_start_date` 로부터 매번 계산 (서버 시간 기준).
- **월별/누적 근무시간**도 저장하지 않고 `service_log.service_hours` 를 서비스 레이어에서 집계.

### 필수서류 ↔ 제출 문서 매칭 (중요)

- **마스터 (정의)**: `document_requirement` 테이블 — `(target_type, document_name, valid_period_years)`. 분류별로 어떤 서류가 필수인지 정의한다.
- **인스턴스 (제출물)**: `document` 테이블 — 실제 업로드된 파일 메타데이터. `requirement_id` FK 로 마스터를 가리킨다.
- **누락 판정 로직**: 특정 client/assistant 에 대해, 해당 `target_type` 의 `document_requirement` 목록 중 `(target_id == 그 client/assistant id)` 이고 `is_submitted == True` 인 `document` 가 없는 항목 = 누락.

### document.status 컬럼 (TODO — 팀 합의 후 추가)

- 현재 `document` 테이블에는 `is_submitted` (BOOLEAN) 만 존재한다.
- 절대규칙 §0.3 의 5종 상태(`미제출 / 제출완료 / 보완필요 / 만료예정 / 만료`)를 보관하려면 `document.status VARCHAR(20)` 컬럼이 필요하다.
- 임의로 추가하지 말고, **팀 합의 후 Alembic 마이그레이션으로 추가**한다. 그 전까지는 `is_submitted` + `expiration_date` 조합과 만료예정 임계값(상수, 30일)으로 서비스 레이어에서 5종을 동적으로 산출한다.

### 10대 핵심 기능 ↔ 코드 매핑

| # | 기능 | 프론트 위치 | 백엔드 라우터 / 모델 |
| --- | --- | --- | --- |
| 1 | 로그인 (직원 전용) | `pages/Login.tsx` | `api/routers/auth.py` / `Staff` |
| 2 | 대시보드 (3 위젯) | `pages/Dashboard.tsx` | `api/routers/dashboard.py` (집계 전용, 모델 없음) |
| 3 | 기관화일 | `pages/AgencyFile.tsx` | `api/routers/document.py` / `Document` |
| 4 | 이용자화일 (서류·메모·이용내역·배정 탭) | `pages/ClientFile.tsx` | `api/routers/client.py` + `document.py` + `service_log.py` + `assignment.py` |
| 5 | 활동지원사화일 (서류·메모·배정 탭) | `pages/AssistantFile.tsx` | `api/routers/assistant.py` + `document.py` + `assignment.py` |
| 6 | 필수서류 체크리스트 | `components/RequiredDocChecklist.tsx` | `api/routers/document.py` / `DocumentRequirement` |
| 7 | 이용내역 관리 | `pages/ServiceLogs.tsx` | `api/routers/service_log.py` / `ServiceLog` |
| 8 | 급여/근속 통합 관리 | `pages/PayrollAndTenure.tsx` | `api/routers/assistant.py` (서비스 레이어에서 근속·시간 집계) |
| 9 | 배정 (별도 페이지 없음 — 이용자/활동지원사 상세 탭에 흡수) | (탭 컴포넌트) | `api/routers/assignment.py` / `Assignment` |
| 10 | 최근 2년치 점검 보기 | `pages/Audit.tsx` | `api/routers/document.py` (2년 필터 적용한 집계) |

> 새 화면/API를 만들기 전에 위 표에서 이미 기능이 있는지 먼저 확인. 같은 기능을 두 곳에 만들지 않는다.

---

## 2. 빌드 / 테스트 (Build / Test)

### Frontend (`frontend/`)
```bash
npm install
npm run dev              # 개발 서버 (Vite, 기본 5173)
npm run build
npm run preview
npm run lint
npm run typecheck        # tsc --noEmit
npm test                 # Vitest 전체
npm test -- <파일경로>   # 단일 테스트 파일
```

### Backend (`backend/`)
```bash
uv sync                                           # 의존성 설치
uvicorn app.main:app --reload --port 8000         # 개발 서버
uv run python -m scripts.seed_staff               # 테스트용 organization + staff 시드
alembic revision --autogenerate -m "<메시지>"     # 마이그레이션 생성
alembic upgrade head                              # DB 적용
pytest                                            # 전체 테스트
pytest tests/test_documents.py::test_upload       # 단일 테스트
ruff check . && ruff format .
```

### Database
- 로컬: MySQL/MariaDB 인스턴스 필요. 접속 정보는 `backend/.env` (커밋 금지).
- 스키마 변경은 **반드시 Alembic 마이그레이션**으로. 직접 SQL `ALTER` 로 수정하지 않는다.

### 통합 실행
- 프론트(5173) ↔ 백엔드(8000) 분리 실행. CORS 는 백엔드에서 허용.
- 프론트 `vite.config.ts` 의 proxy 로 `/api` → `http://localhost:8000` 프록시.

---

## 3. 도메인 컨텍스트 (Domain Context)

### 비즈니스 용어 (영문 매핑)

| 한글 | 영문 (코드) | 비고 |
| --- | --- | --- |
| 기관 | `organization` | 시스템 운영 주체 = 멀티테넌시 루트 |
| 이용자 | `client` | 도메인 의미의 "user". 시스템 로그인 user 와 충돌하므로 `user` 절대 금지. |
| **활동지원사** | **`assistant`** | "worker", "지원사", "도우미" 같은 변형 사용 금지 (2026-05-04 팀 결정 — `assistant` 채택). 이미 만들어진 `worker` 식 식별자가 보이면 정리 대상이다. |
| 사회복지사 / 전담직원 | `staff` | 시스템에 로그인하는 주체 |
| 기관화일 / 이용자화일 / 활동지원사화일 | `document` (단일 테이블) | 어떤 엔티티 소속인지는 `document_requirement.target_type` 으로 구분 |
| 필수서류 정의 | `document_requirement` | `(target_type, document_name, valid_period_years)` 마스터 |
| 이용내역 (전자바우처) | `service_log` | `assignment_id` 로 배정에 종속 |
| 배정 | `assignment` | client ↔ assistant 연결. UI 는 상세 탭. `staff_id` (매칭 담당자) 보유. |
| 근속 | `tenure` | `assistant.work_start_date` 로부터 계산 (저장하지 않음) |
| 급여 | `payroll` | 급여 자동 계산은 비목표. **기초 데이터(월별/누적 시간 + 메모)** 까지만. |
| 메모 (이용자/활동지원사 화일) | `client.client_memo` / `assistant.assistant_memo` | 엔티티당 단일 텍스트, 덮어쓰기. 별도 `notes` 테이블 없음. |
| 메모 (문서 첨부) | `document.document_memo` | 문서별 첨부 메모 |
| 대시보드 | `dashboard` | 집계 전용. 모델 없음. |

> **시스템 로그인 사용자(staff)** 와 **도메인 이용자(client)** 를 코드에서 명확히 분리할 것. 둘 다 `user` 로 부르면 혼란이 생긴다.

### 인증 (JWT 클레임)

- 발급: `POST /api/auth/login` → `{ access_token, token_type: "bearer" }`.
- 페이로드: `{ sub: <staff_id>, organization_id: <int>, exp: <unix_ts> }`.
- 검증: `Depends(get_current_staff)` 가 토큰을 디코드하고, 해당 staff 의 `organization_id` 가 토큰 클레임과 일치하는지 확인한다. 모든 `/api/*` 라우트에 기본 적용한다 (공개 엔드포인트 없음).

### 핵심 데이터 흐름

1. **로그인**: staff 만 로그인 → JWT 발급 → 모든 `/api/*` 요청은 JWT 필수 (대시보드 포함).
2. **신규 등록**: staff 로그인 → 이용자/활동지원사 등록 → 화일에 필수서류 업로드 → `document.is_submitted` 자동 전환 → 5종 상태는 서비스 레이어에서 산출.
3. **배정**: 이용자 욕구 메모(`client.client_memo`) 확인 → 활동지원사 근무 가능 조건(`assistant.work_days`) 확인 → `assignment` 생성 → `service_log` 누적.
4. **점검 대비**: 대시보드 → "최근 2년" 필터 → 미제출/보완필요/만료(예정) 서류 일괄 조회.
5. **만료 처리**: 유효기간 있는 서류는 `document.expiration_date` 보유. 일/주 단위 배치 또는 조회 시점 계산으로 `만료예정`(30일 이내) / `만료` 자동 분류.
6. **메모 흐름**: 이용자/활동지원사 상세 페이지 → "메모" 탭 → 단일 텍스트 컬럼(`*_memo`) 덮어쓰기. 시계열 노트가 필요해지면 그 시점에 별도 테이블을 도입한다 (지금은 만들지 않음).

### 서류 분류 (Week 3 기준)

- 기관화일: 운영문서 / 평가·점검 / 공통양식 / 내부관리
- 이용자화일: 기본서류 / 계약 / 개인정보동의서 / 활동지원급여 제공계획서 / 이용내역서 / 상담·모니터링 / 기타
- 활동지원사화일: 이력서 / 자격·교육 / 근로계약 / 통장사본 / 건강 / 근속 / 기타

이 분류는 **`document_requirement` 마스터의 시드 데이터로** 들어간다 (코드 곳곳에 문자열 리터럴로 흩지 않는다).

---

## 4. 코딩 컨벤션 (Coding Conventions)

### 네이밍

- **Python (백엔드)**: `snake_case` 함수/변수, `PascalCase` 클래스, `UPPER_SNAKE` 상수. 파일명 `snake_case.py`.
- **TypeScript (프론트)**: `camelCase` 함수/변수, `PascalCase` 컴포넌트·타입. 파일명: 컴포넌트 `PascalCase.tsx`, 그 외 `camelCase.ts`.
- **DB 테이블**: `snake_case` 단수형 (예: `client`, `assistant`, `assignment`, `service_log`, `document`, `document_requirement`).
- **DB 컬럼**: **`<엔티티>_<속성>` prefix 패턴** 을 따른다.
  - 예: `client_id`, `client_name`, `client_phone`, `assistant_id`, `assistant_name`, `assistant_memo`, `staff_email`.
  - PK 도 prefix 형태(`client_id`)이며, FK 는 가리키는 PK 이름을 그대로 쓴다(`assignment.client_id` → `client.client_id`).
  - SQLAlchemy 모델에서 Python 속성과 컬럼명은 동일하게 유지(매핑 트릭 없이 1:1).
- **API 경로**: `/api/<resource>` 복수형 케밥 케이스 (예: `/api/clients`, `/api/assistants`, `/api/service-logs`, `/api/document-requirements`).
- **도메인 용어 일관성**: 위 비즈니스 용어 표를 따른다. `client` 대신 `user`, `assistant` 대신 `worker` 를 쓰지 않는다.

### 패턴 규칙

- **상수는 한 곳에 모은다**: 보관기간 5년, 점검 2년, 서류 상태 5종, 만료예정 임계값 30일은 `frontend/src/lib/constants.ts` 와 `backend/app/core/constants.py` 양쪽에 정의하고 동기 유지.
- **서류 상태값은 enum**: TS 는 `as const` 유니온, Python 은 `enum.StrEnum`. 문자열 리터럴을 코드 곳곳에 흩지 않는다.
- **2년/5년 같은 기간 필터는 서비스 레이어**에서 처리. 라우터/컴포넌트에 직접 날짜 계산 로직을 두지 않는다.
- **파일 업로드**는 메타데이터만 DB에 저장하고 실제 파일은 파일시스템(또는 추후 오브젝트 스토리지)에 둔다. DB 에 BLOB 으로 넣지 않는다.
- **메모는 document 와 섞지 않는다**. `client.client_memo` / `assistant.assistant_memo` 는 엔티티 단일 텍스트, `document` 는 파일 메타. 화일 화면에서는 "서류" 탭과 "메모" 탭을 분리한다 (절대규칙 §0.6).
- **인증은 모든 `/api/*` 라우트에 기본 적용**. 의존성 주입(`Depends(get_current_staff)`) 으로 staff 인증을 강제하고, 예외(공개 엔드포인트)를 만들지 않는다. 라우터는 또한 `current_staff.organization_id` 로 쿼리를 필터링해 멀티테넌시를 지킨다.
- **Pydantic 스키마와 SQLAlchemy 모델은 분리**. 모델을 그대로 응답하지 않는다.
- **에러 메시지는 한국어**로 사용자에게 노출 (도메인 사용자는 사회복지사). 단, 로그/예외 클래스 이름은 영문 유지.

### 커밋 컨벤션

- 형식: `<type>: <한국어 또는 영문 한 줄 요약>`
- type: `feat` / `fix` / `refactor` / `docs` / `test` / `chore` / `style`
- 예시:
  - `feat: 이용자 관리명부 CRUD 추가`
  - `fix: 근속기간 계산 시 윤년 처리`
  - `chore: alembic 초기 마이그레이션 생성`
- 한 커밋은 한 가지 일만. 5주 주차 구분이 명확하므로 가능하면 PR/커밋 제목 앞에 `[W2]`, `[W3]` 같은 주차 태그를 붙인다.

---

## 5. 작업 시 우선순위

1. **`plan.md` 를 항상 먼저 확인**한다. 어떤 주차의 어떤 기능을 구현 중인지 명확히 하고 시작한다.
2. 새 기능을 시작하기 전에: 비즈니스 용어 표(섹션 3)와 절대규칙(섹션 0)을 다시 본다.
3. 도메인 모델(특히 `client` / `assistant` / `document` / `document_requirement` / `assignment`) 은 한 번 굳어지면 바꾸기 어려우므로, Week 1 ERD 를 기준으로 신중히 만든다.
4. 노션 "DB / 구조" 문서가 변경되었다는 신호가 보이면, 코드를 고치기 전에 먼저 본 CLAUDE.md 를 동기화한다.
