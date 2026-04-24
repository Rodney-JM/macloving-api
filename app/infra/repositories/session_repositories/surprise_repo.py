from uuid import UUID
from datetime import datetime, timezone

from app.domain.models.session_models.surprise import Surprise, SurpriseStatus
from app.infra.repositories.base import BaseRepository

class SurpriseRepository(BaseRepository[Surprise]):
    model = Surprise
    
    async def get_for_couple(
        self, couple_id: UUID, limit: int = 20, offset: int = 0
    ) -> tuple[list[Surprise], int]:
        filters = [Surprise.couple_id == couple_id]
        items = await self.get_all(
            filters=filters,
            order_by=Surprise.created_at.asc(),
            limit=limit,
            offset=offset
        )
        total = await self.count(*filters)
        return items, total
    
    async def get_unlockable_now(self) -> list[Surprise]:
        now = datetime.now(timezone.utc)
        return await self.get_all(
            filters=[
                Surprise.status == SurpriseStatus.LOCKED,
                Surprise.unlocks_at <= now
            ]
        )