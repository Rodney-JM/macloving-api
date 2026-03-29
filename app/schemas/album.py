from pydantic import BaseModel
from datetime import date, datetime

class AlbumCreate(BaseModel):
    title: str
    description: str | None

class AlbumResponse(BaseModel):
    id: str
    couple_id: str
    title: str
    description: str | None = None
    cover_url: str | None = None
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}