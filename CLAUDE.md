# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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
4. **보관기간 5년·점검 2년 기준은 매직넘버가 아니라 상수**로 관리한다 (한 곳만 수정하면 전체에 반영되도록).

---

## 1. 아키텍처 (Architecture)

### 기술 스택
| 레이어 | 기술 |
| --- | --- |
| Frontend | **React + TypeScript + Vite** |
| Backend | **Python + FastAPI** |
| Database | **MySQL / MariaDB** |
| ORM | SQLAlchemy (권장) + Alembic 마이그레이션 |
| 인증 | JWT 기반 세션 (Week 2 확정) |
| 파일 저장 | 로컬 파일시스템 (MVP), 메타데이터만 DB |

### 권장 폴더 구조
> 아직 코드가 없는 단계이므로 Week 2에서 부트스트랩할 때 아래 구조를 기본으로 한다.

```
소웨공프로젝트/
├── plan.md              # 5주 계획 (단일 출처)
├── CLAUDE.md            # 이 파일
├── frontend/            # React + Vite
│   ├── src/
│   │   ├── pages/       # 화면 단위 (대시보드, 이용자, 활동지원사, 화일, 이용내역…)
│   │   ├── components/  # 공용 UI
│   │   ├── api/         # FastAPI 호출 래퍼
│   │   ├── types/       # 도메인 타입 (User, Worker, Document…)
│   │   └── lib/         # 상수 (서류 상태, 보관기간 등)
│   └── package.json
└── backend/             # FastAPI
    ├── app/
    │   ├── main.py
    │   ├── api/         # 라우터 (users, workers, documents, usage, assignments)
    │   ├── models/      # SQLAlchemy 모델
    │   ├── schemas/     # Pydantic 스키마
    │   ├── services/    # 비즈니스 로직 (근속 계산, 2년 필터, 매칭…)
    │   └── core/        # 설정, DB 세션, 인증
    ├── alembic/
    └── pyproject.toml
```

### 데이터 흐름 핵심
- **3대 화일** (기관/이용자/활동지원사) 은 별도 테이블이 아니라 `documents` 테이블에 `file_type` 컬럼으로 구분 (분류는 `category`).
- **이용자 ↔ 활동지원사**는 `assignments` 테이블로 N:M 관리. 매칭 기준은 이용자 욕구(텍스트) ↔ 활동지원사 근무 가능 요일/시간.
- **2년치 점검 대비 뷰**는 별도 테이블이 아니라 `created_at >= NOW() - INTERVAL 2 YEAR` 필터로 구현.
- **근속기간**은 저장하지 않고 `근무_시작일` 으로부터 매번 계산 (서버 시간 기준).

---

## 2. 빌드 / 테스트 (Build / Test)

> 코드 부트스트랩(Week 2) 이후 사용 가능. 그 전에는 명령어가 동작하지 않는다.

### Frontend (`frontend/`)
```bash
npm install              # 의존성 설치
npm run dev              # 개발 서버 (Vite, 기본 5173)
npm run build            # 프로덕션 빌드
npm run preview          # 빌드 결과 로컬 확인
npm run lint             # ESLint
npm run typecheck        # tsc --noEmit
npm test                 # Vitest 전체
npm test -- <파일경로>   # 단일 테스트 파일
```

### Backend (`backend/`)
```bash
# 가상환경 (uv 또는 venv)
uv sync                                           # 또는 pip install -e .
uvicorn app.main:app --reload --port 8000         # 개발 서버
alembic revision --autogenerate -m "<메시지>"    # 마이그레이션 생성
alembic upgrade head                              # DB 적용
pytest                                            # 전체 테스트
pytest tests/test_documents.py::test_upload       # 단일 테스트
ruff check . && ruff format .                     # 린트/포맷
```

### Database
- 로컬: MySQL/MariaDB 인스턴스 필요. 접속 정보는 `backend/.env` (커밋 금지).
- 스키마 변경은 **반드시 Alembic 마이그레이션**으로. 직접 SQL `ALTER`로 수정하지 않는다.

### 통합 실행
- 프론트(5173) ↔ 백엔드(8000) 분리 실행. CORS는 백엔드에서 허용.
- 프론트 `vite.config.ts`의 proxy로 `/api` → `http://localhost:8000` 프록시.

---

## 3. 도메인 컨텍스트 (Domain Context)

### 비즈니스 용어 (영문 매핑)
| 한글 | 영문 (코드) | 비고 |
| --- | --- | --- |
| 기관 | `agency` / `organization` | 시스템 운영 주체 |
| 이용자 | `user` (도메인 의미) / 코드에서는 `client` 권장 | 시스템 로그인 user와 충돌 주의 |
| 활동지원사 | `worker` | "지원사", "도우미" 같은 변형 사용 금지 |
| 사회복지사 / 전담직원 | `staff` | 시스템에 로그인하는 주체 |
| 기관화일 | `agency_file` | 문서 분류값 |
| 이용자화일 | `client_file` | |
| 활동지원사화일 | `worker_file` | |
| 이용내역 (전자바우처) | `service_log` / `usage_log` | |
| 배정 | `assignment` | 이용자 ↔ 활동지원사 연결 |
| 근속 | `tenure` | 근무 시작일로부터 계산 |
| 필수서류 | `required_document` | 분류별로 필수 목록 정의 |

> **시스템 로그인 사용자(staff)** 와 **도메인 이용자(client)** 를 코드에서 명확히 분리할 것. 둘 다 `user` 로 부르면 혼란이 생긴다.

### 핵심 데이터 흐름
1. **신규 등록 흐름**: staff 로그인 → 이용자/활동지원사 등록 → 화일에 필수서류 업로드 → 상태 자동 `미제출`→`제출완료` 전환.
2. **배정 흐름**: 이용자 욕구 메모 확인 → 활동지원사 근무 가능 조건 확인 → 배정 생성 → 이용내역 누적.
3. **점검 대비 흐름**: 대시보드 → "최근 2년" 필터 → 미제출/보완필요/만료(예정) 서류 일괄 조회.
4. **만료 처리**: 유효기간 있는 서류는 `expire_at` 컬럼 보유. 일/주 단위 배치 또는 조회 시점 계산으로 `만료예정`(30일 이내) / `만료` 자동 분류.

### 서류 분류 (Week 3 기준)
- 기관화일: 운영문서 / 평가·점검 / 공통양식 / 내부관리
- 이용자화일: 기본서류 / 계약 / 개인정보동의서 / 활동지원급여 제공계획서 / 이용내역서 / 상담·모니터링 / 기타
- 활동지원사화일: 이력서 / 자격·교육 / 근로계약 / 통장사본 / 건강 / 근속 / 기타

---

## 4. 코딩 컨벤션 (Coding Conventions)

### 네이밍
- **Python (백엔드)**: `snake_case` 함수/변수, `PascalCase` 클래스, `UPPER_SNAKE` 상수. 파일명 `snake_case.py`.
- **TypeScript (프론트)**: `camelCase` 함수/변수, `PascalCase` 컴포넌트·타입. 파일명: 컴포넌트 `PascalCase.tsx`, 그 외 `camelCase.ts`.
- **DB 테이블/컬럼**: `snake_case` 단수형 권장 (예: `client`, `worker`, `assignment`, `service_log`).
- **API 경로**: `/api/<resource>` 복수형 케밥 케이스 (예: `/api/clients`, `/api/service-logs`, `/api/required-documents`).
- **도메인 용어 일관성**: 위 비즈니스 용어 표를 따른다. `client` 대신 `user`를 도메인 의미로 쓰지 않는다.

### 패턴 규칙
- **상수는 한 곳에 모은다**: 보관기간 5년, 점검 2년, 서류 상태 5종, 만료예정 임계값(30일 등)은 `frontend/src/lib/constants.ts` 와 `backend/app/core/constants.py` 양쪽에 정의하고 동기 유지.
- **서류 상태값은 enum**: TS는 `as const` 유니온, Python은 `enum.StrEnum`. 문자열 리터럴을 코드 곳곳에 흩지 않는다.
- **2년/5년 같은 기간 필터는 서비스 레이어**에서 처리. 라우터/컴포넌트에 직접 날짜 계산 로직을 두지 않는다.
- **파일 업로드**는 메타데이터만 DB에 저장하고 실제 파일은 파일시스템(또는 추후 오브젝트 스토리지)에 둔다. DB에 BLOB으로 넣지 않는다.
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

1. **`plan.md`를 항상 먼저 확인**한다. 어떤 주차의 어떤 기능을 구현 중인지 명확히 하고 시작한다.
2. 새 기능을 시작하기 전에: 비즈니스 용어 표(섹션 3)와 절대규칙(섹션 0)을 다시 본다.
3. 도메인 모델(특히 `client` / `worker` / `document` / `assignment`)은 한 번 굳어지면 바꾸기 어려우므로, Week 1 ERD를 기준으로 신중히 만든다.
