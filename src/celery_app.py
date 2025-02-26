import datetime
import os
import asyncio

import redis
from celery import Celery
from pinecone import Pinecone, ServerlessSpec

from src.parser import fetch_sitemap
from src.fetch_html import fetch_html, extract_text_from_html, vectorize_text


celery = Celery(
    "tasks",
    broker=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://redis:6379/0")
)

redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = "sitemap-vector"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=300,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(index_name)

async def process_urls_async(urls):

    if not urls:
        return {"No new urls to parse": "All urls in sitemap.xml are already in database"}

    html_response = await asyncio.gather(*(fetch_html(url) for url in urls))
    tasks = []
    for url, html in zip(urls, html_response):

        cleaned_text = extract_text_from_html(html)
        vector = vectorize_text(cleaned_text).tolist()

        point_id = abs(hash(url)) % (10 ** 10)
        metadata = {"url": url, "text": cleaned_text[:500]}

        tasks.append(asyncio.to_thread(lambda: index.upsert([(str(point_id), vector, metadata)])))


    await asyncio.gather(*tasks)

    return {"message": "finished"}


@celery.task
def process_sitemap(sitemap_url):

    redis_client.set("status", "PARSING")
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        urls = loop.run_until_complete(fetch_sitemap(sitemap_url))
        result = loop.run_until_complete(process_urls_async(urls))

        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

        redis_client.set(
            "status",
            f"FINISHED: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        )

    except Exception as e:
        redis_client.set(
            "status",
            f"ERROR {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        )
        raise e

    return result
