from contextlib import asynccontextmanager

import uvicorn
from backend.core import (
    AppDIContainer,
    AppDIProxy,
    Settings,
    create_engine,
    create_session_maker,
)
from backend.core.database import create_all_table
from backend.internal.passport.handler import passport_router
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    engine = create_engine(settings.database_url)
    session_maker = create_session_maker(engine=engine)
    AppDIProxy.initialize(AppDIContainer(settings=settings, session_maker=session_maker))
    await create_all_table(engine=engine)
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
