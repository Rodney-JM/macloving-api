from pydantic import BaseModel
from datetime import datetime
from app.application.schemas.user import UserResponse

class CoupleResponse(BaseModel):
    id: str
    created_at: datetime
    members: list[UserResponse] = []
    model_config = {"from_attributes": True}