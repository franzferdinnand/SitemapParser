import os
import qdrant_client

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from qdrant_client.http.models import VectorParams, Distance
from qdrant_client.models import PointStruct

from fetch_html import fetch_html, extract_text_from_html, vectorize_text
from src.parser import fetch_sitemap

router = APIRouter()
status = {"last_run": "None"}
client = qdrant_client.QdrantClient(host=os.getenv("QDRANT_HOST", "localhost"), port=os.getenv("QDRANT_PORT", 6333))


class ParseRequest(BaseModel):
    url: str

@router.post("/parse")
async def parse(request: ParseRequest):
    status["last_run"] = "running"

    urls = await fetch_sitemap(request.url)
    for url in urls:
        html = await fetch_html(url)
        cleaned_text = extract_text_from_html(html)
        vector = vectorize_text(cleaned_text)
        point = PointStruct(vector=vector, id=hash(url), payload={"url": url, "text": cleaned_text})
        client.upsert(collection_name=os.getenv("COLLECTION_NAME", "sitemap_vector"), points=[point])

    status["last_run"] = "finished"
    return {"parsing is finished"}

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


