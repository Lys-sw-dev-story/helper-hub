"""document.needs_revision 컬럼 추가 마이그레이션 (멱등).

W4 백로그 #11 — 서류 5종 상태 자동 분류 도입에 따라 보완필요 플래그를 추가한다.

실행:
    cd backend
    uv run python -m scripts.migrate_document_needs_revision

이미 컬럼이 있으면 아무 동작도 하지 않는다.
"""

from __future__ import annotations

import sys

from sqlalchemy import inspect, text

from app.core.database import engine


COLUMN_NAME = "needs_revision"
TABLE_NAME = "document"


def migrate() -> None:
    inspector = inspect(engine)
    if TABLE_NAME not in inspector.get_table_names():
        print(f"[migrate] '{TABLE_NAME}' 테이블이 없습니다. 먼저 서버를 한 번 띄워 create_all 을 실행하세요.")
        return

    columns = {col["name"] for col in inspector.get_columns(TABLE_NAME)}
    if COLUMN_NAME in columns:
        print(f"[migrate] '{TABLE_NAME}.{COLUMN_NAME}' 이미 존재 — skip")
        return

    with engine.begin() as conn:
        conn.execute(
            text(
                f"ALTER TABLE `{TABLE_NAME}` "
                f"ADD COLUMN `{COLUMN_NAME}` TINYINT(1) NOT NULL DEFAULT 0"
            )
        )
    print(f"[migrate] '{TABLE_NAME}.{COLUMN_NAME}' 추가 완료")


if __name__ == "__main__":
    try:
        migrate()
    except Exception as exc:
        print(f"[migrate] 실패: {exc}", file=sys.stderr)
        sys.exit(1)
