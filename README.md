🏠 Helper-Hub
사회복지사를 위한 이용자-조력자 매칭 및 행정 관리 시스템

🛠 Tech Stack
Frontend: React (Vite), TypeScript, CSS Modules
Backend: Python (FastAPI), uv(Package Manager)
Database: MySQL
🚀 시작하기
1. Repository 클론
git clone [https://github.com/Lys-sw-dev-story/helper-hub.git](https://github.com/Lys-sw-dev-story/helper-hub.git)
cd helper-hub

### 2. 사전 설치
프로젝트 구동을 위해 아래 도구들이 필요합니다.

Node.js: React 프론트엔드 구동을 위해 필요합니다.
uv (Python Manager): 고성능 파이썬 패키지 및 가상환경 관리를 위해 사용합니다.

PowerShell 설치 명령어:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

### 3. backend 설정
cd backend
uv sync
cp .env.example .env
# 생성된 .env 파일 내의 MySQL 비밀번호를 본인 환경에 맞게 수정해주세요.

# 서버 실행
uv run uvicorn app.main:app --reload

### 3. Frontend 설정 (Nodde.js)
cd frontend
npm install
npm run dev

### 4. 서버 접속
http://localhost:5173/