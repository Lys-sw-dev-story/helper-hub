"""문서 분류 마스터(document_requirement) 시드 스크립트."""

from __future__ import annotations
import sys
from app.core.constants import DocumentTargetType
from app.core.database import Base, SessionLocal, engine
from app.models import (
    assignment,
    assistant,
    client,
    document,
    document_requirement,
    organization,
    service_log,
    staff,
)
from app.models.document_requirement import DocumentRequirement

SEED_DATA: list[tuple[DocumentTargetType, str, int | None]] = [
    # 이용자화일
    (DocumentTargetType.CLIENT, "A", 1),
    (DocumentTargetType.CLIENT, "B", 1),
    (DocumentTargetType.CLIENT, "C", 1),
    # 활동지원사화일
    (DocumentTargetType.ASSISTANT, "a", 1),
    (DocumentTargetType.ASSISTANT, "b", 1),
    (DocumentTargetType.ASSISTANT, "c", 1),
]

def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = {
            (row.target_type, row.document_name)
            for row in db.query(DocumentRequirement).all()
        }
        created = 0
        for target_type, document_name, valid_years in SEED_DATA:
            key = (target_type.value, document_name)
            if key in existing:
                continue
            db.add(
                DocumentRequirement(
                    target_type=target_type.value,
                    document_name=document_name,
                    valid_period_years=valid_years,
                )
            )
            created += 1
        db.commit()
        print(f"[seed] document_requirement 신규 {created}건 추가 (기존 {len(existing)}건 유지)")
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