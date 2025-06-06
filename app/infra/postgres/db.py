from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from typing_extensions import AsyncGenerator

from app.config import settings

engine = create_async_engine(url=settings.postgres_uri)

session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with session_maker() as session:
        yield session


GetSessionDep = Annotated[AsyncSession, Depends(get_session)]
