from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ✅ CORS 미들웨어 가져오기
from app.api.api import api_router
from app.core.database import engine, Base

from app.models import (
    organization, staff, client, assistant,
    assignment, service_log, document, document_requirement
)

app = FastAPI(title="Helper-Hub API")

# ✅ CORS 허용할 프론트엔드 주소 세팅
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# ✅ FastAPI 앱에 CORS 예외 허가증 부착
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # 프론트엔드 개발 서버 주소 허용
    allow_credentials=True,           # 토큰 인증 정보 허용
    allow_methods=["*"],              # GET, POST, PUT, DELETE 등 모든 요청 허용
    allow_headers=["*"],              # 모든 HTTP 헤더 허용
)

# 서버 시작 시 테이블 생성 (이미 있으면 생성 안 함)
Base.metadata.create_all(bind=engine)

# 중복 등록되어 있던 라우터 코드를 하나로 깔끔하게 정리 완료!
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Helper Hub API가 정상 작동 중입니다!"}

def main():
    print("Hello from backend!")


if __name__ == "__main__":
    main()