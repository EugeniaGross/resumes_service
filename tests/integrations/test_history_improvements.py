from httpx import AsyncClient
import pytest

from .fixtures.base import ac, setup_test_db


@pytest.mark.asyncio
async def test_improve_resume_with_token(ac: AsyncClient):
    payload = {"title": "Test Resume", "content": "Original content"}
    create_resp = await ac.post(
        "/api/v1/resumes/", json=payload, headers={"Authorization": "Bearer"}
    )
    resume_id = create_resp.json()["id"]
    response = await ac.post(
        f"/api/v1/resumes/{resume_id}/improve", headers={"Authorization": "Bearer"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "Improved" in data["improved_content"]
    assert data["resume_id"] == resume_id


@pytest.mark.asyncio
async def test_improve_nonexistent_resume(ac: AsyncClient):
    response = await ac.post(
        "/api/v1/resumes/9999/improve",
        headers={"Authorization": "Bearer"},
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Резюме не найдено"


@pytest.mark.asyncio
async def test_improve_resume_without_token(ac: AsyncClient):
    response = await ac.post("/api/v1/resumes/1/improve")
    assert response.status_code == 401
