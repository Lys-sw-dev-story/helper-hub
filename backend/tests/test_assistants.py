"""활동지원사(assistant) CRUD + organization 격리 회귀 테스트."""
from __future__ import annotations


def test_unauthenticated_request_is_rejected(api):
    resp = api.get("/api/assistants/")
    assert resp.status_code == 401


def test_create_returns_id_and_name(api, auth_headers_a):
    resp = api.post(
        "/api/assistants/",
        json={"assistant_name": "이몽룡", "work_days": "월,화,수"},
        headers=auth_headers_a,
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["assistant_name"] == "이몽룡"
    assert isinstance(body["assistant_id"], int)


def test_list_returns_only_own_organization(api, auth_headers_a, auth_headers_b):
    api.post(
        "/api/assistants/", json={"assistant_name": "A기관-지원사"}, headers=auth_headers_a
    )
    api.post(
        "/api/assistants/", json={"assistant_name": "B기관-지원사"}, headers=auth_headers_b
    )

    resp_a = api.get("/api/assistants/", headers=auth_headers_a)
    assert resp_a.status_code == 200
    names_a = [a["assistant_name"] for a in resp_a.json()]
    assert names_a == ["A기관-지원사"]

    resp_b = api.get("/api/assistants/", headers=auth_headers_b)
    names_b = [a["assistant_name"] for a in resp_b.json()]
    assert names_b == ["B기관-지원사"]


def test_get_returns_full_detail(api, auth_headers_a):
    created = api.post(
        "/api/assistants/",
        json={
            "assistant_name": "이몽룡",
            "assistant_phone": "010-0000-0002",
            "work_days": "월,수,금",
            "work_start_date": "2025-01-02",
        },
        headers=auth_headers_a,
    ).json()
    aid = created["assistant_id"]

    resp = api.get(f"/api/assistants/{aid}", headers=auth_headers_a)
    assert resp.status_code == 200
    body = resp.json()
    assert body["assistant_name"] == "이몽룡"
    assert body["assistant_phone"] == "010-0000-0002"
    assert body["work_days"] == "월,수,금"
    assert body["work_start_date"] == "2025-01-02"


def test_get_other_organization_returns_404(api, auth_headers_a, auth_headers_b):
    aid = api.post(
        "/api/assistants/", json={"assistant_name": "A기관-지원사"}, headers=auth_headers_a
    ).json()["assistant_id"]

    resp = api.get(f"/api/assistants/{aid}", headers=auth_headers_b)
    assert resp.status_code == 404


def test_patch_updates_only_supplied_fields(api, auth_headers_a):
    aid = api.post(
        "/api/assistants/",
        json={"assistant_name": "옛이름", "work_days": "월"},
        headers=auth_headers_a,
    ).json()["assistant_id"]

    resp = api.patch(
        f"/api/assistants/{aid}",
        json={"work_days": "월,수,금"},
        headers=auth_headers_a,
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["assistant_name"] == "옛이름"
    assert body["work_days"] == "월,수,금"


def test_patch_other_organization_returns_404(api, auth_headers_a, auth_headers_b):
    aid = api.post(
        "/api/assistants/", json={"assistant_name": "A기관-지원사"}, headers=auth_headers_a
    ).json()["assistant_id"]

    resp = api.patch(
        f"/api/assistants/{aid}",
        json={"work_days": "월"},
        headers=auth_headers_b,
    )
    assert resp.status_code == 404


def test_delete_removes_record(api, auth_headers_a):
    aid = api.post(
        "/api/assistants/", json={"assistant_name": "삭제대상"}, headers=auth_headers_a
    ).json()["assistant_id"]

    resp = api.delete(f"/api/assistants/{aid}", headers=auth_headers_a)
    assert resp.status_code == 204

    after = api.get(f"/api/assistants/{aid}", headers=auth_headers_a)
    assert after.status_code == 404


def test_delete_other_organization_returns_404(api, auth_headers_a, auth_headers_b):
    aid = api.post(
        "/api/assistants/", json={"assistant_name": "A기관-지원사"}, headers=auth_headers_a
    ).json()["assistant_id"]

    resp = api.delete(f"/api/assistants/{aid}", headers=auth_headers_b)
    assert resp.status_code == 404

    still_there = api.get(f"/api/assistants/{aid}", headers=auth_headers_a)
    assert still_there.status_code == 200
