# celery_app.py
import asyncio

from celery import Celery
import os
from src.parser import fetch_sitemap
from src.fetch_html import fetch_html, extract_text, vectorize_text
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct


celery = Celery(
    "tasks",
    broker=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://redis:6379/0")
)

client = QdrantClient(host=os.getenv("QDRANT_HOST", "localhost"), port=int(os.getenv("QDRANT_PORT", 6333)))

def process_urls(urls):
    for url in urls:
        html = fetch_html(url)
        cleaned_text = extract_text(html)
        vector = vectorize_text(cleaned_text)
        point = PointStruct(id=hash(url), vector=vector, payload={"url": url, "text": cleaned_text})
        client.upsert(collection_name=os.getenv("COLLECTION_NAME", "sitemap_vector"), points=[point])

    return {"message": "Парсинг завершено"}

@celery.task
def process_sitemap(sitemap_url):
    global status
    status["last_run"] = "running"
    urls = asyncio.run(fetch_sitemap(sitemap_url))
    result = process_urls(urls)
    status["last_run"] = "finished"
    return result
