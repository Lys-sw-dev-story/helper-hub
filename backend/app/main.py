from fastapi import FastAPI
from app.core.database import engine, Base
from app.api.api import api_router

# 중요!!: Base.metadata가 인지할 수 있도록 모든 모델을 여기서 import 해야 함
from app.models import (
    organization, staff, client, assistant, 
    assignment, service_log, document, document_requirement
)

app = FastAPI(title="Helper-Hub API")
app.include_router(api_router)

# 서버 시작 시 테이블 생성 (이미 있으면 생성 안 함)
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Helper Hub API가 정상 작동 중입니다!"}

def main():
    print("Hello from backend!")


if __name__ == "__main__":
    main()