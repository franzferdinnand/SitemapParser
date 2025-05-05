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
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── sitemaps/                    # Input XML sitemaps
├── src/
│   ├── main.py                  # FastAPI entry point
│   ├── parser.py                # Async sitemap parsing logic
│   ├── vector_store.py          # Pinecone integration
│   ├── cache.py                 # Redis caching functions
│   ├── db.py                    # MongoDB connection and operations
│   └── routes/                  # FastAPI endpoint definitions
└── README.md
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

> 📂 Place your `.xml` sitemap files in the `sitemaps/` directory.

## 🔗 Example API Usage

- Upload a sitemap for parsing:
  ```
  POST /upload-sitemap
  Body: { "filename": "sitemaps/my_sitemap.xml" }
  ```

- List parsed URLs:
  ```
  GET /urls
  ```

## 🧠 Semantic Search

The project uses **sentence embeddings** to represent URLs and stores them as vectors in **Pinecone**. This allows semantic similarity search — finding URLs that are conceptually related, not just exact text matches.

## 🧑‍💻 Author

Developed by [Serhii Turchyn](https://github.com/franzferdinnand)

## 📝 License

This project is licensed under the [MIT License](LICENSE).