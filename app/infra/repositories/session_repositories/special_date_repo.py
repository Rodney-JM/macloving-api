from datetime import datetime, timezone

from uuid import UUID
from sqlalchemy import select

from app.domain.models.session_models.special_date import SpecialDate
from app.infra.repositories.base import BaseRepository

class SpecialDateRepository(BaseRepository[SpecialDate]):
    model = SpecialDate
    
    async def get_by_couple(self, couple_id: UUID) -> list[SpecialDate]:
        return await self.get_all(
            filters=[SpecialDate.couple_id == couple_id],
            order_by=SpecialDate.event_date.asc()
        )
        
    async def get_next_upcoming(self, couple_id: UUID) -> SpecialDate | None:
        now = datetime.now(timezone.utc)
        result = await self.session.execute(
            select(SpecialDate)
            .where(
                SpecialDate.couple_id == couple_id,
                SpecialDate.event_date >=now
            )
            .order_by(SpecialDate.event_date.asc())
            .limit(1)
        )
        return result.scalar_one_or_none()
    
    