import datetime
import os
import asyncio
from celery import Celery
from pinecone import Pinecone, ServerlessSpec

from src.parser import fetch_sitemap
from src.fetch_html import fetch_html, extract_text_from_html, vectorize_text

status = {"last_run": "None"}

celery = Celery(
    "tasks",
    broker=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://redis:6379/0")
)

# Ініціалізація Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = "sitemap-vector"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=300,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")  # Або інший регіон, якщо потрібно
    )

index = pc.Index(index_name)


async def process_urls_async(urls):

    for url in urls:
        html = await fetch_html(url)
        cleaned_text = extract_text_from_html(html)
        vector = vectorize_text(cleaned_text).tolist()

        point_id = abs(hash(url)) % (10 ** 10)
        metadata = {"url": url, "text": cleaned_text[:500]}

        index.upsert([(str(point_id), vector, metadata)])

    return {"message": "finished"}


@celery.task
def process_sitemap(sitemap_url):
    """Celery Task для обробки sitemap."""
    global status
    status["last_run"] = "running"

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    urls = loop.run_until_complete(fetch_sitemap(sitemap_url))
    result = loop.run_until_complete(process_urls_async(urls))

    status["last_run"] = f"finished {datetime.datetime.now()}"

    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()

    return result
