import httpx
from config import settings

_client: httpx.AsyncClient | None = None

async def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        headers = {}
        if settings.API_KEY:
            headers["Authorization"] = f"Bearer {settings.API_KEY}"
        _client = httpx.AsyncClient(base_url=settings.API_BASE, headers=headers, timeout=10.0)
    return _client

async def close_client():
    global _client
    if _client:
        await _client.aclose()
        _client = None
