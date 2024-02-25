from httpx import AsyncClient
import pytest

from main import my_app


@pytest.mark.anyio
async def test_user():
    async with AsyncClient(app=my_app, base_url="http://test") as ac:
        response = await ac.get("/user")
    assert response.status_code == 307


@pytest.mark.anyio
async def test_create_user():
    async with AsyncClient(app=my_app, base_url="http://test") as ac:
        response = ac.post(
            "/user/",
            json={
                "first_name": "vlad",
                "last_name": "mialkin",
                "email": "mialkin@example.com",
                "date_of_birth": "2000-02-25"
            }
        )
