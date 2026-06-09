"""유효기간 정의가 있는데 만료일이 비어 있는 제출 문서에 만료일을 채운다 (멱등).

규칙: expiration_date = created_date + requirement.valid_period_years (년)
  - requirement.valid_period_years 가 없거나 0 이면 유효기간 없는 서류 → 건드리지 않음
  - 이미 expiration_date 가 있으면 건너뜀(덮어쓰지 않음)
  - created_date 가 없으면 계산 불가 → 건너뜀(로그만)

데모용으로 점검 대비 화면의 '만료(예정)일'이 비어 보이는 문제를 메운다.

실행:
    cd backend
    uv run python -m scripts.backfill_document_expiration
"""

from __future__ import annotations

import sys
from datetime import date

from app.core.database import SessionLocal
from app.models import (  # noqa: F401  매퍼 관계 해석을 위한 전체 모델 등록
    assignment,
    assistant,
    client,
    document,
    document_requirement,
    organization,
    service_log,
    staff,
)
from app.models.document import Document
from app.models.document_requirement import DocumentRequirement


def _add_years(base: date, years: int) -> date:
    """base + years. 윤년(2/29)이면 day=28 로 떨어뜨린다 (audit_service 와 동일 규칙)."""
    try:
        return base.replace(year=base.year + years)
    except ValueError:
        return base.replace(year=base.year + years, day=28)


def backfill() -> None:
    db = SessionLocal()
    filled = 0
    skipped_no_created = 0
    try:
        reqs = {r.requirement_id: r for r in db.query(DocumentRequirement).all()}

        for doc in db.query(Document).all():
            req = reqs.get(doc.requirement_id)
            if req is None:
                continue
            vpy = req.valid_period_years
            # 유효기간 없는 서류이거나, 미제출이거나, 이미 만료일이 있으면 대상 아님
            if not doc.is_submitted or not vpy or vpy <= 0:
                continue
            if doc.expiration_date is not None:
                continue
            if doc.created_date is None:
                skipped_no_created += 1
                print(
                    f"[backfill] doc={doc.document_id} \"{req.document_name}\" "
                    "작성일 없음 → 계산 불가, 건너뜀"
                )
                continue

            new_exp = _add_years(doc.created_date, vpy)
            doc.expiration_date = new_exp
            filled += 1
            print(
                f"[backfill] doc={doc.document_id} \"{req.document_name}\" "
                f"작성일={doc.created_date} +{vpy}년 → 만료일={new_exp}"
            )

        db.commit()
        print(
            f"[backfill] 완료 — {filled}건 채움"
            + (f", {skipped_no_created}건 계산불가" if skipped_no_created else "")
        )
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    try:
        backfill()
    except Exception as exc:
        print(f"[backfill] 실패: {exc}", file=sys.stderr)
        sys.exit(1)
