from fastapi import FastAPI

from src.routes import router

app = FastAPI(title="SitemapParser")

app.include_router(router)
