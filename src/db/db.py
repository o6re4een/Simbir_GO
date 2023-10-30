import setting
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase


# Engine to interact with db
engine = create_async_engine("postgresql+asyncpg://postgres:root@localhost:5432/simbir", pool_pre_ping=True)

# session with interaction
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_async_session():
    async with async_session_maker() as session:
        yield session
