from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from dotenv import load_dotenv
import os

load_dotenv()
engine = create_async_engine(url=os.getenv('POSTGRES'))

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    chat_id = mapped_column(BigInteger)


class Post(Base):
    __tablename__ = 'posts'

    post_id: Mapped[int] = mapped_column(primary_key=True)
    email = mapped_column(String(30))
    password = mapped_column(String(190))
    user_id: Mapped[int] = mapped_column(ForeignKey(column='users.user_id', ondelete='CASCADE'))


class Rule(Base):
    __tablename__ = 'rules'

    rule_id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey(column='posts.post_id', ondelete='CASCADE'))
    email = mapped_column(String(30))
    action = mapped_column(String(20))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
