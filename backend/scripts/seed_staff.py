"""테스트용 organization + staff 시드 스크립트.

실행 방법:
    cd backend
    uv run python -m scripts.seed_staff

기본 비밀번호: admin1234 (모든 계정 동일)
"""

from __future__ import annotations

import sys

from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models import (  # noqa: F401  Base.metadata 인지를 위한 import
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

# 🚀 데모를 위한 기관 리스트 및 소속 사회복지사 데이터 정의
DEMO_DATA = [
    {
        "org_name": "기관 A",
        "staffs": [
            {"email": "adminA1@example.com", "name": "김복지 (A팀장)", "role": "사회복지사"},
            {"email": "adminA2@example.com", "name": "이복지 (A행정)", "role": "사회복지사"},
            {"email": "adminA3@example.com", "name": "박복지 (A실무)", "role": "사회복지사"},
        ]
    },
    {
        "org_name": "기관 B",
        "staffs": [
            {"email": "adminB1@example.com", "name": "최복지 (B팀장)", "role": "사회복지사"},
            {"email": "adminB2@example.com", "name": "정복지 (B행정)", "role": "사회복지사"},
            {"email": "adminB3@example.com", "name": "강복지 (B실무)", "role": "사회복지사"},
        ]
    },
    {
        "org_name": "기관 C",
        "staffs": [
            {"email": "adminC1@example.com", "name": "조복지 (C팀장)", "role": "사회복지사"},
            {"email": "adminC2@example.com", "name": "윤복지 (C행정)", "role": "사회복지사"},
            {"email": "adminC3@example.com", "name": "장복지 (C실무)", "role": "사회복지사"},
        ]
    }
]

COMMON_PASSWORD = "admin1234"


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        password_hash = hash_password(COMMON_PASSWORD)
        
        for data in DEMO_DATA:
            org_name = data["org_name"]
            
            # 1. 기관 조회 또는 생성
            org = db.query(Organization).filter(Organization.organization_name == org_name).first()
            if org is None:
                org = Organization(organization_name=org_name)
                db.add(org)
                db.flush()  # ID 확보를 위해 flush
                print(f"[seed] organization 생성 완료: id={org.organization_id}, name={org.organization_name}")
            else:
                print(f"[seed] organization 이미 존재: id={org.organization_id}, name={org.organization_name}")
            
            # 2. 해당 기관에 3명의 staff 매핑 및 생성
            for staff_info in data["staffs"]:
                existing_staff = db.query(Staff).filter(Staff.staff_email == staff_info["email"]).first()
                
                if existing_staff is None:
                    new_staff = Staff(
                        staff_email=staff_info["email"],
                        staff_password_hash=password_hash,
                        staff_name=staff_info["name"],
                        staff_role=staff_info["role"],
                        organization_id=org.organization_id,
                    )
                    db.add(new_staff)
                    print(f"  -> [staff 생성] {staff_info['name']} ({staff_info['email']})")
                else:
                    print(f"  -> [staff 존재] {existing_staff.staff_name} ({existing_staff.staff_email})")
                    
        db.commit()
        print("\n==================================================")
        print("🎉 모든 데모용 기관 및 사회복지사 시드 데이터 삽입 완료!")
        print(f"🔑 모든 계정 로그인 비밀번호: {COMMON_PASSWORD}")
        print("==================================================")

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