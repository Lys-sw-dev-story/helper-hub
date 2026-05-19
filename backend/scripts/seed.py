"""테스트용 필수 데이터(Organization + Staff) 시드 스크립트.

실행 방법:
    cd backend
    uv run python -m scripts.seed

기본 계정: admin@example.com / admin1234 (개발용 더미값)
"""

from __future__ import annotations

import sys

from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models import (  # noqa: F401  Base.metadata 인지를 위한 전체 모델 임포트 구조 유지
    assignment,
    assistant,
    client,
    document,
    document_requirement,
    organization,
    service_log,
    staff,
)
from app.models.organization import Organization
from app.models.staff import Staff


SEED_ORGANIZATION_NAME = "홍길동복지관"
SEED_STAFF_EMAIL = "admin@example.com"
SEED_STAFF_PASSWORD = "admin1234"
SEED_STAFF_NAME = "홍길동"
SEED_STAFF_ROLE = "사회복지사"


def seed() -> None:
    # 1. 뼈대가 되는 모든 MySQL 테이블 자동 생성 (없을 때만 생성됨)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        print("🌱 필수 기초 데이터(기관 및 직원 계정) 시딩을 시작합니다...")

        # 2. 기관(Organization) 데이터 확인 및 생성
        org = (
            db.query(Organization)
            .filter(Organization.organization_name == SEED_ORGANIZATION_NAME)
            .first()
        )
        if org is None:
            org = Organization(organization_name=SEED_ORGANIZATION_NAME)
            db.add(org)
            db.flush()  # staff 생성을 위해 상위 organization의 ID를 먼저 확보
            print(f"[seed] organization 생성 완료: id={org.organization_id} name={org.organization_name}")
        else:
            print(f"[seed] organization 이미 존재: id={org.organization_id}")

        # 3. 직원(Staff) 로그인 계정 확인 및 생성
        existing = (
            db.query(Staff).filter(Staff.staff_email == SEED_STAFF_EMAIL).first()
        )
        if existing is not None:
            print(f"[seed] staff 이미 존재: id={existing.staff_id} email={existing.staff_email}")
            db.commit()
            return

        new_staff = Staff(
            staff_email=SEED_STAFF_EMAIL,
            staff_password_hash=hash_password(SEED_STAFF_PASSWORD),  # FastAPI Bcrypt 암호화 연동
            staff_name=SEED_STAFF_NAME,
            staff_role=SEED_STAFF_ROLE,
            organization_id=org.organization_id,
        )
        db.add(new_staff)
        db.commit()
        db.refresh(new_staff)
        
        print(
            "[seed] staff 생성 완료: "
            f"id={new_staff.staff_id} email={new_staff.staff_email} "
            f"organization_id={new_staff.organization_id}"
        )
        print(f"[seed] 테스트 비밀번호: {SEED_STAFF_PASSWORD}")
        print("🎉 필수 데이터 시딩이 성공적으로 완료되었습니다!")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    try:
        seed()
    except Exception as exc:
        print(f"[seed] 실패: {exc}", file=sys.stderr)
        sys.exit(1)