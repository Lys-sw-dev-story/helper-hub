"""이용자(client) CRUD + organization 격리 회귀 테스트."""
from __future__ import annotations


def test_unauthenticated_request_is_rejected(api):
    resp = api.get("/api/clients/")
    assert resp.status_code == 401


def test_create_returns_id_and_name(api, auth_headers_a):
    resp = api.post(
        "/api/clients/",
        json={"client_name": "홍길동", "client_status": "신규"},
        headers=auth_headers_a,
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["client_name"] == "홍길동"
    assert isinstance(body["client_id"], int)


def test_list_returns_only_own_organization(api, auth_headers_a, auth_headers_b):
    api.post("/api/clients/", json={"client_name": "A기관-이용자"}, headers=auth_headers_a)
    api.post("/api/clients/", json={"client_name": "B기관-이용자"}, headers=auth_headers_b)

    resp_a = api.get("/api/clients/", headers=auth_headers_a)
    assert resp_a.status_code == 200
    names_a = [c["client_name"] for c in resp_a.json()]
    assert names_a == ["A기관-이용자"]

    resp_b = api.get("/api/clients/", headers=auth_headers_b)
    names_b = [c["client_name"] for c in resp_b.json()]
    assert names_b == ["B기관-이용자"]


def test_get_returns_full_detail(api, auth_headers_a):
    created = api.post(
        "/api/clients/",
        json={
            "client_name": "홍길동",
            "client_phone": "010-0000-0001",
            "client_status": "이용중",
        },
        headers=auth_headers_a,
    ).json()
    cid = created["client_id"]

    resp = api.get(f"/api/clients/{cid}", headers=auth_headers_a)
    assert resp.status_code == 200
    body = resp.json()
    assert body["client_name"] == "홍길동"
    assert body["client_phone"] == "010-0000-0001"
    assert body["client_status"] == "이용중"


def test_get_other_organization_returns_404(api, auth_headers_a, auth_headers_b):
    cid = api.post(
        "/api/clients/", json={"client_name": "A기관-이용자"}, headers=auth_headers_a
    ).json()["client_id"]

    resp = api.get(f"/api/clients/{cid}", headers=auth_headers_b)
    assert resp.status_code == 404


def test_patch_updates_only_supplied_fields(api, auth_headers_a):
    cid = api.post(
        "/api/clients/",
        json={"client_name": "옛이름", "client_status": "신규"},
        headers=auth_headers_a,
    ).json()["client_id"]

    resp = api.patch(
        f"/api/clients/{cid}",
        json={"client_status": "이용중"},
        headers=auth_headers_a,
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["client_name"] == "옛이름"
    assert body["client_status"] == "이용중"


def test_patch_other_organization_returns_404(api, auth_headers_a, auth_headers_b):
    cid = api.post(
        "/api/clients/", json={"client_name": "A기관-이용자"}, headers=auth_headers_a
    ).json()["client_id"]

    resp = api.patch(
        f"/api/clients/{cid}",
        json={"client_status": "이용중"},
        headers=auth_headers_b,
    )
    assert resp.status_code == 404


def test_delete_removes_record(api, auth_headers_a):
    cid = api.post(
        "/api/clients/", json={"client_name": "삭제대상"}, headers=auth_headers_a
    ).json()["client_id"]

    resp = api.delete(f"/api/clients/{cid}", headers=auth_headers_a)
    assert resp.status_code == 204

    after = api.get(f"/api/clients/{cid}", headers=auth_headers_a)
    assert after.status_code == 404


def test_delete_other_organization_returns_404(api, auth_headers_a, auth_headers_b):
    cid = api.post(
        "/api/clients/", json={"client_name": "A기관-이용자"}, headers=auth_headers_a
    ).json()["client_id"]

    resp = api.delete(f"/api/clients/{cid}", headers=auth_headers_b)
    assert resp.status_code == 404

    still_there = api.get(f"/api/clients/{cid}", headers=auth_headers_a)
    assert still_there.status_code == 200
