# SitemapParser 🕸️

**SitemapParser** is an asynchronous Python-based service designed to parse XML sitemap files, extract URLs, and store them in a structured, searchable format. The system supports caching, semantic vectorization, and offers a REST API for interaction. It’s built with modern technologies including FastAPI, MongoDB, Redis, and Pinecone for scalable vector search.

## 🧰 Tech Stack

- **Python 3.10+**
- **FastAPI** – high-performance web framework for building APIs
- **asyncio + aiohttp** – asynchronous architecture for efficient I/O
- **MongoDB** – document-based database for persistent URL storage
- **aioredis** – asynchronous caching layer
- **Pinecone** – vector database for semantic search
- **Docker / Docker Compose** – containerization and service orchestration

## ⚙️ Features

- Asynchronous parsing of `.xml` sitemap files
- URL extraction from `<loc>` tags
- Caching results with Redis
- Storage of parsed data in MongoDB
- Semantic embedding of URLs and vector storage in Pinecone
- REST API to:
  - upload and process sitemap files
  - list all parsed URLs
  - perform semantic search on URLs

## 📁 Project Structure

```
SitemapParser/
├── .env # Environment variables
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── LICENSE
├── src/
│ ├── main.py # FastAPI app entry point
│ ├── routes.py # API routes
│ ├── parser.py # Sitemap XML parsing
│ ├── fetch_html.py # Async HTML fetching
│ ├── database.py # MongoDB and Redis setup
│ ├── celery_app.py # Celery worker
│ └── addons/ # Additional modules
```

## 🔧 Environment Variables

Below is a description of the environment variables used in the project. Create a .env file in the root of the repository with the following variables:

```
# URL to the XML sitemap to parse
SITEMAP_URL=https://sitemaps.org/sitemap.xml

# Redis configuration for caching and Celery broker
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_CACHE_STORAGE_TIME=3600
REDIS_URL=redis://redis:6379/0

# FastAPI application settings
FASTAPI_APP_HOST=localhost
FASTAPI_APP_PORT=8000

# Pinecone vector database configuration
PINECONE_HOST=pinecone
PINECONE_PORT=7000
PINECONE_API_KEY=<your-pinecone-api-key>
PINECONE_INDEX_NAME=sitemap_vector

# MongoDB configuration
MONGO_DB_URI=mongodb://mongo_db:27017
MONGO_DB_NAME=sitemap_parser

# Flower dashboard for Celery task monitoring
FLOWER_PORT=5555

# Celery broker configuration
CELERY_BROKER_URL=redis://redis:6379/0

# Ensures logs are output immediately (useful for Docker)
PYTHONUNBUFFERED=1

```

## 🚀 Getting Started

1. Clone the repository:

```bash
git clone https://github.com/franzferdinnand/SitemapParser.git
cd SitemapParser
```

2. Start the services using Docker Compose:

```bash
docker compose up --build
```

## 🔗 Example API Usage

- Upload a sitemap for parsing:
  ```
  POST /parse
  Body: { "url": "your sitemap url" }
  ```

- See Parser Status:
  ```
  GET /status
  ```

## 🧠 Semantic Search

The project uses **sentence embeddings** to represent URLs and stores them as vectors in **Pinecone**. This allows semantic similarity search — finding URLs that are conceptually related, not just exact text matches.

## 🧑‍💻 Author

Developed by [Serhii Turchyn](https://github.com/franzferdinnand)

## 📝 License

This project is licensed under the [MIT License](LICENSE).