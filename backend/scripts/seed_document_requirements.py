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
    # 이용자화일 (이용자 분류 — CLAUDE.md §3 서류 분류 기준)
    (DocumentTargetType.CLIENT, "이용자 기본서류", None),
    (DocumentTargetType.CLIENT, "계약 관련 서류", None),
    (DocumentTargetType.CLIENT, "개인정보 동의서", None),
    (DocumentTargetType.CLIENT, "활동지원급여 제공계획서", 1),
    (DocumentTargetType.CLIENT, "이용내역서", None),
    (DocumentTargetType.CLIENT, "상담/모니터링 기록", None),
    (DocumentTargetType.CLIENT, "기타 증빙서류", None),
    # 활동지원사화일 (활동지원사 분류)
    (DocumentTargetType.ASSISTANT, "이력서", None),
    (DocumentTargetType.ASSISTANT, "자격/교육 이수 관련 서류", None),
    (DocumentTargetType.ASSISTANT, "근로계약 관련 서류", None),
    (DocumentTargetType.ASSISTANT, "통장사본", None),
    (DocumentTargetType.ASSISTANT, "건강 관련 서류", 1),
    (DocumentTargetType.ASSISTANT, "근속 관련 서류", None),
    (DocumentTargetType.ASSISTANT, "기타 증빙서류", None),
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