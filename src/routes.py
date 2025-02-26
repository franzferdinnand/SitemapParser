import os
from redis import asyncio as aioredis

from fastapi import APIRouter
from pydantic import BaseModel

from src.database import delete_database
from src.celery_app import process_sitemap


router = APIRouter()
redis_client = aioredis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))


class ParseRequest(BaseModel):
    url: str

@router.post("/parse")
async def parse(request: ParseRequest):
    await redis_client.set("status", "PARSING")
    task = process_sitemap.delay(request.url)
    return {
        "task_id": task.id,
        "status": await redis_client.get("status")
    }

@router.get("/status")
async def get_status():
    status = await redis_client.get("status")
    return {"status": status}

@router.delete("/delete")
async def reset_database():
    await delete_database()
    await redis_client.set("status", "waiting")
    return {"database is deleted"}
