from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.db.base import Base

ModelT = TypeVar("ModelT", bound=Base)

class BaseRepository(Generic[ModelT]):
    model: type[ModelT]
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    async def get_by_id(self, id: UUID) -> ModelT | None:
        return await self.session.get(self.model, id)

    async def get_all(
        self,
        *,
        filters: list[Any] | None = None,
        order_by: Any | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[ModelT]:
        stmt = select(self.model)
        if filters:
            stmt = stmt.where(*filters)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        stmt = stmt.limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def count(self, *filters: Any) -> int:
        stmt = select(func.count()).select_from(self.model)
        if filters:
            stmt = stmt.where(*filters)
        result = await self.session.execute(stmt)
        return result.scalar_one()
    
    async def add(self, instance: ModelT) -> ModelT:
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance
    
    async def delete(self, instance: ModelT) -> None:
        await self.session.delete(instance)
        await self.session.flush()
    
    async def bulk_add(self, instances: list[ModelT]) -> None:
        self.session.add_all(instances)
        await self.session.flush()