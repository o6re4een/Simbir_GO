
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from setting import REAL_DB_URL

# Engine to interact with db
# print(REAL_DB_URL)
engine = create_async_engine(REAL_DB_URL, pool_pre_ping=True, echo=True, future=True)


# session with interaction
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


  

class Base(DeclarativeBase):
    pass


async def get_async_session():
    async with async_session_maker() as session:
        yield session
