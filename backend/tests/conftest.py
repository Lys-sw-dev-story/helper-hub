"""테스트 공용 픽스처.

- production MySQL engine을 SQLite in-memory engine으로 monkeypatch한 뒤 app.main을 import
- 매 테스트마다 모든 테이블 drop/create 로 격리
- 두 organization + 각각의 staff + JWT 헤더 픽스처 제공 (멀티테넌시 검증용)
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import BigInteger, create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.core.database as db_module


# SQLite는 BIGINT PRIMARY KEY를 rowid alias로 인식하지 않아 autoincrement가 동작하지 않는다.
# 운영 DB(MySQL)에는 영향이 없고, 테스트(SQLite)에서만 BigInteger를 INTEGER로 발행하도록 한다.
@compiles(BigInteger, "sqlite")
def _bigint_to_integer_for_sqlite(element, compiler, **kw):  # noqa: ANN001
    return "INTEGER"

TEST_ENGINE = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)

db_module.engine = TEST_ENGINE
db_module.SessionLocal = TestSessionLocal

from app.core.database import Base, get_db  # noqa: E402
from app.core.security import create_access_token, hash_password  # noqa: E402
from app.main import app  # noqa: E402
from app.models.organization import Organization  # noqa: E402
from app.models.staff import Staff  # noqa: E402


def _override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture(autouse=True)
def _reset_database():
    Base.metadata.drop_all(bind=TEST_ENGINE)
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield


@pytest.fixture
def db_session():
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def api(db_session):
    with TestClient(app) as test_client:
        yield test_client


def _make_staff(db_session, organization_name: str, email: str) -> Staff:
    org = Organization(organization_name=organization_name)
    db_session.add(org)
    db_session.commit()
    db_session.refresh(org)

    staff = Staff(
        staff_email=email,
        staff_password_hash=hash_password("password1234"),
        staff_name="더미직원",
        staff_role="사회복지사",
        organization_id=org.organization_id,
    )
    db_session.add(staff)
    db_session.commit()
    db_session.refresh(staff)
    return staff


@pytest.fixture
def staff_a(db_session) -> Staff:
    return _make_staff(db_session, "A복지관", "staff_a@example.com")


@pytest.fixture
def staff_b(db_session) -> Staff:
    return _make_staff(db_session, "B복지관", "staff_b@example.com")


def _auth_headers(staff: Staff) -> dict[str, str]:
    token = create_access_token(
        subject=staff.staff_id,
        organization_id=staff.organization_id,
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers_a(staff_a) -> dict[str, str]:
    return _auth_headers(staff_a)


@pytest.fixture
def auth_headers_b(staff_b) -> dict[str, str]:
    return _auth_headers(staff_b)
