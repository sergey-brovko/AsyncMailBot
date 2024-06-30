from database.models import async_session
from sqlalchemy import select, update
from database.models import User, Post, Rule
import datetime


async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.chat_id == tg_id))

        if not user:
            session.add(User(chat_id=tg_id))
            await session.commit()


