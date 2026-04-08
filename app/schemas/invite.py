from pydantic import BaseModel
from datetime import datetime

class InviteResponse(BaseModel):
    token: str
    expires_at: datetime
    
class InviteAccept(BaseModel):
    token: str
    
    