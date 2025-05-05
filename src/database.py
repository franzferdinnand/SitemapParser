import os
import motor.motor_asyncio


MONGO_URI = os.getenv("MONGO_DB_URI",  "mongodb://mongo_db:27017")

def get_mongo_client():
    return motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

async def get_database():
    client = get_mongo_client()
    return client[os.getenv("MONGO_DB_NAME", "sitemap_parser")]

async def create_indexes():
    db = await get_database()
    collection = db.urls
    await collection.create_index("url", unique=True)

async def url_is_parsed(url:str):
    db = await get_database()
    collection = db["urls"]

    return await collection.find_one({"url": url})

async def save_url(url:str):
    db = await get_database()
    collection = db["urls"]
    if not await url_is_parsed(url):
        await collection.insert_one({"url": url})

async def delete_database():
    client = get_mongo_client()
    await client.drop_database(os.getenv("MONGO_DB_NAME", "sitemap_parser"))
