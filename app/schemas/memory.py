from pydantic import BaseModel
from datetime import date, datetime

class MemoryCreate(BaseModel):
    title: str | None = None
    note: str | None = None
    memory_date: date | None = None
    media_type: str | None = None
    
class MemoryResponse(BaseModel):
    id: str 
    album_id: str
    author_id: str
    title: str | None = None
    note: str | None = None
    memory_date: date | None = None
    media_url: str | None = None
    thumbnail_url: str | None = None
    media_type: str | None = None
    created_at: datetime 
    
    model_config = {"from_attributes": True}