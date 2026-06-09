"""매칭 태그 컬럼 추가 마이그레이션 (멱등).

W5 — 이용자 ↔ 활동지원사 태그 매칭 도입에 따라 태그 저장 컬럼을 추가한다.

추가 컬럼 (CSV 문자열 저장, 예: "월,수,금" / "신체활동 지원,사회활동 지원"):
    - client.client_preferred_days  VARCHAR(50)   희망 요일
    - client.client_support_types   VARCHAR(100)  희망 지원 분야
    - assistant.assistant_support_types VARCHAR(100)  가능 지원 분야
    (assistant.work_days 는 기존 컬럼을 그대로 요일 태그로 사용)

실행:
    cd backend
    uv run python -m scripts.migrate_matching_tags

이미 컬럼이 있으면 해당 컬럼은 건너뛴다.
"""

from __future__ import annotations

import sys

from sqlalchemy import inspect, text

from app.core.database import engine


# (table, column, ddl_type)
COLUMNS: list[tuple[str, str, str]] = [
    ("client", "client_preferred_days", "VARCHAR(50)"),
    ("client", "client_support_types", "VARCHAR(100)"),
    ("assistant", "assistant_support_types", "VARCHAR(100)"),
]


def migrate() -> None:
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    for table_name, column_name, ddl_type in COLUMNS:
        if table_name not in existing_tables:
            print(
                f"[migrate] '{table_name}' 테이블이 없습니다. "
                "먼저 서버를 한 번 띄워 create_all 을 실행하세요."
            )
            continue

        columns = {col["name"] for col in inspector.get_columns(table_name)}
        if column_name in columns:
            print(f"[migrate] '{table_name}.{column_name}' 이미 존재 — skip")
            continue

        with engine.begin() as conn:
            conn.execute(
                text(
                    f"ALTER TABLE `{table_name}` "
                    f"ADD COLUMN `{column_name}` {ddl_type} NULL"
                )
            )
        print(f"[migrate] '{table_name}.{column_name}' 추가 완료")


if __name__ == "__main__":
    try:
        migrate()
    except Exception as exc:
        print(f"[migrate] 실패: {exc}", file=sys.stderr)
        sys.exit(1)
