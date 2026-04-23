from app.domain.models.memory import Memory
from app.infra.repositories.base import BaseRepository

class MemoryRepository(BaseRepository[Memory]):
    model = Memory