from uuid import UUID
from datetime import date
from sqlalchemy import select

from app.domain.models.ritual import RitualEntry
from app.infra.repositories.base import BaseRepository

class RitualEntryRepository(BaseRepository[RitualEntry]):
    model = RitualEntry
    
    async def get_today_entries(
        self, ritual_id: UUID, today:date
    ) -> list[RitualEntry]:
        return await self.get_all(
            filters=[
                RitualEntry.ritual_id == ritual_id,
                RitualEntry.entry_date == today
            ]
        )
        
    async def get_user_entry_today(
        self, ritual_id: UUID, user_id: UUID, today: date
    ) -> RitualEntry | None:
        result = await self.session.execute(
            select(RitualEntry).where(
                RitualEntry.ritual_id == ritual_id,
                RitualEntry.user_id == user_id,
                RitualEntry.entry_date == today
            )
        )
        
        return result.scalar_one_or_none()
    
    async def get_history(
        self, ritual_id: UUID, limit: int = 30, offset: int = 0
    ) -> list[RitualEntry]:
        return await self.get_all(
            filters=[RitualEntry.ritual_id == ritual_id],
            order_by=RitualEntry.entry_date.desc(),
            limit=limit,
            offset=offset
        )