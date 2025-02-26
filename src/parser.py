import aiohttp
from fastapi import HTTPException
import xml.etree.ElementTree as ET

from src.database import url_is_parsed, save_url


async def fetch_sitemap(sitemap_url:str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(sitemap_url) as response:
                if response.status != 200:
                    raise HTTPException(status_code=response.status, detail="unable to download Sitemap")
                xml_data = await response.text()
                return await parse_sitemap(xml_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def parse_sitemap(xml_data:str):
    try:
        root = ET.fromstring(xml_data)
        urls = []
        for elem in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
            url = elem.text.strip()
            if not await url_is_parsed(url):
                await save_url(url)
                urls.append(url)
        return urls
    except ET.ParseError:
        raise HTTPException(status_code=400, detail="Error in parse sitemap.xml")
