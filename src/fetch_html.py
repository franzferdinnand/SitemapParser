import os

import aiohttp
import redis.asyncio as aioredis
import spacy

from fastapi import HTTPException
from selectolax.parser import HTMLParser


REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
redis = None

nlp = spacy.load("en_core_web_md")

async def connect_redis():
    global redis
    if redis is None:
        redis = await aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
    return redis

async def fetch_html(url:str):
    redis_connection = await connect_redis()
    cached_response = await redis_connection.get(url)

    if cached_response:
        return cached_response

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise HTTPException(status_code=response.status, detail="unable to download Sitemap")
                await redis_connection.set(url, response.text, ex=os.getenv("REDIS_CACHE_STORAGE_TIME", 3600))
                return await response.text()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def extract_text_from_html(html_text:str):
    tree = HTMLParser(html_text)
    for tag in ["script", "style", "nav", "footer", "aside", "header"]:
        for node in tree.css(tag):
            node.decompose()
    text = "\n".join(node.text(strip=True) for node in tree.css("p, h1, h2, h3, h4, h5, h6, li, blockquote"))
    return text.strip()

def vectorize_text(text:str):
    return nlp(text).vector