from pydantic import BaseModel
from typing import List
from integrations.api_client import get_client

class Service(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float | None = None
    duration_minutes: int | None = None
    is_active: bool

class PageServices(BaseModel):
    items: List[Service]
    total: int
    page: int
    size: int

async def list_services(page: int = 1, size: int = 8, active: bool = True) -> PageServices:
    client = await get_client()
    resp = await client.get("/services", params={"active": str(active).lower(), "page": page, "size": size})
    resp.raise_for_status()
    data = resp.json()
    return PageServices(**data)
