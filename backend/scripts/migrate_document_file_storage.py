"""document 테이블에 파일 DB 저장용 컬럼 추가 (수동 마이그레이션).

팀 결정(2026-06-02): 파일을 파일시스템이 아니라 DB(LONGBLOB)에 저장한다.
이 프로젝트는 Alembic을 쓰지 않고 create_all 로 테이블을 만들기 때문에, 기존 테이블에는
컬럼이 자동 추가되지 않는다. 그래서 이 스크립트로 ALTER 한다. 여러 번 실행해도 안전하다.

추가 컬럼:
- file_name VARCHAR(255)  : 원본 파일명
- file_data LONGBLOB      : 실제 파일 바이트
"""

from __future__ import annotations

import sys

from sqlalchemy import inspect, text

from app.core.database import engine

TABLE = "document"
COLUMNS = {
    "file_name": "VARCHAR(255) NULL",
    "file_data": "LONGBLOB NULL",
}


def run() -> None:
    inspector = inspect(engine)
    existing = {col["name"] for col in inspector.get_columns(TABLE)}

    to_add = {name: ddl for name, ddl in COLUMNS.items() if name not in existing}
    if not to_add:
        print("[migrate] 추가할 컬럼 없음 (이미 적용됨)")
        return

    with engine.begin() as conn:
        for name, ddl in to_add.items():
            conn.execute(text(f"ALTER TABLE {TABLE} ADD COLUMN {name} {ddl}"))
            print(f"[migrate] {TABLE}.{name} 추가 ({ddl})")

    print(f"[migrate] 완료 — {len(to_add)}개 컬럼 추가")


if __name__ == "__main__":
    try:
        run()
    except Exception as exc:  # noqa: BLE001
        print(f"[migrate] 실패: {exc}", file=sys.stderr)
        sys.exit(1)
