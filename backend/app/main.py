from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.api.api import api_router

from app.models import (
    organization, staff, client, assistant,
    assignment, service_log, document, document_requirement
)

app = FastAPI(title="Helper-Hub API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 프론트엔드(Vite) 주소 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 방식(GET, POST, OPTIONS 등) 허용
    allow_headers=["*"],  # 모든 헤더 허용
)
app.include_router(api_router)

# 서버 시작 시 테이블 생성 (이미 있으면 생성 안 함)
Base.metadata.create_all(bind=engine)

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Helper Hub API가 정상 작동 중입니다!"}

def main():
    print("Hello from backend!")


if __name__ == "__main__":
    main()