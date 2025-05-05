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


async def get_redis_connection():
    return await aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", decode_responses=True)

async def fetch_html(url:str):
    redis_connection = await get_redis_connection()
    cached_response = await redis_connection.get(url)

    if cached_response:
        return cached_response

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise HTTPException(status_code=response.status, detail="unable to download Sitemap")
                html_content = await response.text()
                await redis_connection.set(url, html_content, ex=int(os.getenv("REDIS_CACHE_STORAGE_TIME", 3600)))
                return html_content
    except Exception as e:
        raise ValueError(f"error {e}")

def extract_text_from_html(html_text:str):
    tree = HTMLParser(html_text)
    for tag in ["script", "style", "nav", "footer", "aside", "header"]:
        for node in tree.css(tag):
            node.decompose()
    text = " ".join(node.text(strip=True) for node in tree.css("p, h1, h2, h3, h4, h5, h6, li, blockquote"))
    clean_text = text.replace("\n", " ")
    return clean_text.strip()

def vectorize_text(text:str):
    return nlp(text).vector