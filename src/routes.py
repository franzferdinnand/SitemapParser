import os

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

from src.parser import fetch_sitemap

router = APIRouter()

status = {"last_run": "None"}

class SitemapRequest(BaseModel):
    url: str

@router.post("/parse")
async def parse_sitemap(request: SitemapRequest):
    sitemap_url = request.url or os.getenv("SITEMAP_URL")
    if not sitemap_url:
        raise HTTPException(status_code=400, detail="Sitemap url is not provided")
    urls = await fetch_sitemap(sitemap_url)
    return urls

@router.get("/status")
def get_status():
    return status

@router.delete("/delete")
def reset_database():
    ...

async def parser_task():
    import asyncio
    await asyncio.sleep(3)
    status["last_run"] = "Parser is done"

