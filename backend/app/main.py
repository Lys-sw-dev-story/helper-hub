from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.core.database import engine, Base

# Base.metadata가 인지할 수 있도록 모든 모델을 여기서 import
from app.models import (
    organization,
    staff,
    client,
    assistant,
    assignment,
    service_log,
    document,
    document_requirement,
)

app = FastAPI(title="Helper-Hub API")

# 프론트엔드 개발 서버 CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 서버 시작 시 테이블 생성 (이미 있으면 생성 안 함)
Base.metadata.create_all(bind=engine)

# API 라우터 등록
app.include_router(api_router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Helper Hub API가 정상 작동 중입니다!"}


def main():
    print("Hello from backend!")


if __name__ == "__main__":
    main()