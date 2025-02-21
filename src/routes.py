import os
import qdrant_client

from fastapi import APIRouter
from pydantic import BaseModel
from qdrant_client.http.models import VectorParams, Distance

from src.celery_app import process_urls


router = APIRouter()
status = {"last_run": "None"}
client = qdrant_client.QdrantClient(host=os.getenv("QDRANT_HOST", "localhost"), port=os.getenv("QDRANT_PORT", 6333))


class ParseRequest(BaseModel):
    url: str

@router.post("/parse")
async def parse(request: ParseRequest):
    status["last_run"] = "running"
    task = process_urls.delay(request.url)
    status["task_id"] = task.id
    return {"status": status["last_run"], "task_id": task.id}

@router.get("/status")
def get_status():
    return status

@router.delete("/delete")
def reset_database():
    client.delete_collection(collection_name=os.getenv("COLLECTION_NAME", "sitemap_vector"))
    client.create_collection(
        collection_name=os.getenv("COLLECTION_NAME", "sitemap_vector"),
        vectors_config= {"default": VectorParams(size=384, distance=Distance.COSINE)},
    )
    status["last_run"] = "None"
    return {"database is deleted"}


