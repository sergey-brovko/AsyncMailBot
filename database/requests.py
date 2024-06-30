from database.models import async_session
from sqlalchemy import select, update
from database.models import User, Mailbox, Rule
from encryption.crypt import encrypt, decrypt


async def set_user(chat_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.chat_id == chat_id))

        if not user:
            session.add(User(chat_id=chat_id))
            await session.commit()


async def set_mailbox(chat_id: int, email: str, password: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.chat_id == chat_id))
        if user:
            session.add(Mailbox(user_id=user.user_id, email=email, password=encrypt(password)))
            await session.commit()


async def get_mailboxes(chat_id: int) -> Mailbox:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.chat_id == chat_id))
        return await session.scalars(select(Mailbox).where(Mailbox.user_id == user.user_id).order_by(Mailbox.email))
