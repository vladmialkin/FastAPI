from sqlalchemy import select, insert

from conftest import client, async_session_test
from app.db.models import User


def test_create_user():
    client.post("/user/", json=
    {
        "first_name": "string",
        "last_name": "string",
        "email": "user@example.com",
        "date_of_birth": "2024-02-24"

    })


async def test_get_users():
    async with async_session_test() as session:
        query = insert(User).values(first_name='vlad', last_name="mialkin", email="vladmialkin@example.com",
                                    date_of_birth="2000-02-24")
        await session.execute(query)
        await session.commit()

        query = select(User)
        result = await session.execute(query)
        print(result.all())
