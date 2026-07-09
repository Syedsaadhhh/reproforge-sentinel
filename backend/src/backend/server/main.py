from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from backend.core import (
    AppDIContainer,
    AppDIProxy,
    Settings,
    create_engine,
    create_session_maker,
)
from backend.internal.passport.handler import passport_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    engine = create_engine(settings.database_url)
    session_maker = create_session_maker(engine=engine)
    AppDIProxy.initialize(AppDIContainer(settings=settings, session_maker=session_maker))
    yield
    AppDIProxy.clear()


app = FastAPI(lifespan=lifespan)
app.include_router(passport_router)

if __name__ == "__main__":
    uvicorn.run(
        "backend.server.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
