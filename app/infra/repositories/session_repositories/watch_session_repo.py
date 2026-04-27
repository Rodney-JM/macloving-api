from uuid import UUID

from sqlalchemy import select
from app.domain.models.session_models.watch_session import WatchSession
from app.infra.repositories.base import BaseRepository

class WatchSessionRepository(BaseRepository[WatchSession]):
    model = WatchSession
    
    async def get_active_for_couple(self, couple_id: UUID) -> WatchSession | None:
        result = await self.session.execute(
            select(WatchSession).where(
                WatchSession.couple_id == couple_id,
                WatchSession.ended_at == None,
            ).order_by(WatchSession.created_at.desc()).limit(1)
        )
        
        return result.scalar_one_or_none()