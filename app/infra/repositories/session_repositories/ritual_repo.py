from uuid import UUID

from app.domain.models.ritual import Ritual
from app.infra.repositories.base import BaseRepository

class RitualRepository(BaseRepository[Ritual]):
    model = Ritual
    
    async def get_active_by_couple(self, couple_id: UUID) -> list[Ritual]:
        return await self.get_all(
            filters=[Ritual.couple_id == couple_id, Ritual.is_active == True],
            order_by=Ritual.created_at.asc()
        )