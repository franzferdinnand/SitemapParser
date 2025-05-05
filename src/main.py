from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import create_indexes
from src.routes import router

@asynccontextmanager
async def lifespan(application: FastAPI):
    await create_indexes()
    yield

app = FastAPI(lifespan=lifespan, title="SitemapParser")

app.include_router(router)

