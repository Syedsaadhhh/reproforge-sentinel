from __future__ import annotations

from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from typing import Any

    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

    from . import Settings


@dataclass(frozen=True)
class AppDIContainer:
    """
    The container which hold all dependency for server
    If we use FastAPI's inbuilt `Depends` feature which slowdown the server, we don't need this
    """

    settings: Settings
    session_maker: async_sessionmaker[AsyncSession]

    @asynccontextmanager
    async def get_db_session(self):
        async with self.session_maker() as session:
            async with session.begin():
                yield session


class AppDIProxy:
    """
    This will a place holder for `AppDIContainer`. All di related exception check done here
    to avoid repetative code in top order.
    """

    _app_di_container: AppDIContainer | None = None

    @classmethod
    def initialize(cls, container: AppDIContainer):
        cls._app_di_container = container

    @classmethod
    def clear(cls):
        cls._app_di_container = None

    def is_initialized(self):
        return AppDIProxy._app_di_container is not None

    def __getattr__(self, name: str):
        if AppDIProxy._app_di_container is None:
            raise ValueError("DI container is not initialized")
        return getattr(AppDIProxy._app_di_container, name)

    def __setattr__(self, name: str, value: Any):
        if AppDIProxy._app_di_container is None:
            raise
        return setattr(AppDIProxy._app_di_container, name, value)


app_dependency = cast(AppDIContainer, AppDIProxy())
