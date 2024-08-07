from sqlalchemy import BigInteger, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
import os

engine = create_async_engine(url=os.getenv('POSTGRES_URL'))

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    chat_id = mapped_column(BigInteger)
    receive_letters = mapped_column(Boolean, default=False)


class Mailbox(Base):
    __tablename__ = 'mailboxes'

    mailbox_id: Mapped[int] = mapped_column(primary_key=True)
    email = mapped_column(String(30))
    password = mapped_column(String(190))
    user_id: Mapped[int] = mapped_column(ForeignKey(column='users.user_id', ondelete='CASCADE'))


class Rule(Base):
    __tablename__ = 'rules'

    rule_id: Mapped[int] = mapped_column(primary_key=True)
    mailbox_id: Mapped[int] = mapped_column(ForeignKey(column='mailboxes.mailbox_id', ondelete='CASCADE'))
    email = mapped_column(String(30))
    action = mapped_column(String(20))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
