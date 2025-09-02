from httpx import AsyncClient
import pytest

from .fixtures.base import ac, setup_test_db
from application.main import app


@pytest.mark.asyncio
async def test_create_resume_with_token(ac: AsyncClient):
    payload = {"title": "Test Resume", "content": "Some content"}
    response = await ac.post(
        "/api/v1/resumes/", json=payload, headers={"Authorization": "Bearer"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]


@pytest.mark.asyncio
async def test_create_resume_without_token(ac: AsyncClient):
    payload = {"title": "Test Resume", "content": "Some content"}
    response = await ac.post(
        "/api/v1/resumes/",
        json=payload,
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_resumes_with_token(ac: AsyncClient):
    response = await ac.get("/api/v1/resumes/", headers={"Authorization": "Bearer"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_list_resumes_without_token(ac: AsyncClient):
    response = await ac.get("/api/v1/resumes/")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_resume_with_token(ac: AsyncClient):
    payload = {"title": "Resume 1", "content": "Content 1"}
    create_resp = await ac.post(
        "/api/v1/resumes/", json=payload, headers={"Authorization": "Bearer"}
    )
    resume_id = create_resp.json()["id"]
    response = await ac.get(
        f"/api/v1/resumes/{resume_id}", headers={"Authorization": "Bearer"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == resume_id
    assert data["title"] == payload["title"]


@pytest.mark.asyncio
async def test_get_resume_without_token(ac: AsyncClient):
    response = await ac.get("/api/v1/resumes/1")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_resume_with_token(ac: AsyncClient):
    payload = {"title": "Original", "content": "Original content"}
    create_resp = await ac.post(
        "/api/v1/resumes/", json=payload, headers={"Authorization": "Bearer"}
    )
    resume_id = create_resp.json()["id"]
    update_payload = {"title": "Updated", "content": "Updated content"}
    response = await ac.patch(
        f"/api/v1/resumes/{resume_id}",
        json=update_payload,
        headers={"Authorization": "Bearer"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_payload["title"]
    assert data["content"] == update_payload["content"]


@pytest.mark.asyncio
async def test_update_resume_without_token(ac: AsyncClient):
    update_payload = {"title": "Updated", "content": "Updated content"}
    response = await ac.patch("/api/v1/resumes/1", json=update_payload)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_resume_with_token(ac: AsyncClient):
    payload = {"title": "To delete", "content": "Content"}
    create_resp = await ac.post(
        "/api/v1/resumes/", json=payload, headers={"Authorization": "Bearer"}
    )
    resume_id = create_resp.json()["id"]
    response = await ac.delete(
        f"/api/v1/resumes/{resume_id}", headers={"Authorization": "Bearer"}
    )
    assert response.status_code == 204
    get_resp = await ac.get(
        f"/api/v1/resumes/{resume_id}", headers={"Authorization": "Bearer"}
    )
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_resume_without_token(ac: AsyncClient):
    response = await ac.delete("/api/v1/resumes/1")
    assert response.status_code == 401
