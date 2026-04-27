from uuid import UUID

from app.domain.models.session_models.letter import Letter, LetterStatus
from app.infra.repositories.base import BaseRepository

class LetterRepository(BaseRepository[Letter]):
    model = Letter
    
    async def get_for_couple(
        self, 
        couple_id:UUID,
        *,
        limit: int = 20,
        offset: int = 0
    ) -> tuple[list[Letter], int]:
        filters = [Letter.couple_id == couple_id]
        items = await self.get_all(
            filters=filters,
            order_by=Letter.created_at.desc(),
            limit=limit,
            offset=offset
        )
        
        total = await self.count(*filters)
        return items, total
    
    async def get_unread_count(self, recipient_id: UUID) -> int:
        return await self.count(
            Letter.recipient_id == recipient_id,
            Letter.status == LetterStatus.SENT
        )
    