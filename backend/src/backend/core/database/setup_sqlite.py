from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine


def create_engine(database_url: str):
    engine = create_async_engine(
        database_url,
        connect_args={"check_same_thread": False},
        poolclass=NullPool,
    )
    return engine


def create_session_maker(engine: AsyncEngine):
    async_session_maker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    return async_session_maker
