from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.schemas.common import PaginatedResponse
from app.application.schemas.memory import MemoryResponse, MemoryUpdateRequest, MemoryUploadRequest
from app.application.services.domain_services.memory_service import MemoryService
from app.core.dependencies.auth import require_couple
from app.core.dependencies.rate_limit import RateLimit
from app.domain.enums.memory_category import MemoryCategory
from app.domain.models.user import User
from app.infra.db.session import get_db_session

router = APIRouter(prefix="/memories", tags=["Memories"])

CoupleUser = Annotated[User, Depends(require_couple)]


@router.post("", response_model=MemoryResponse, status_code=status.HTTP_201_CREATED)
async def create_memory(
    user: CoupleUser,
    _: RateLimit,
    file: UploadFile = File(...),
    album_id: UUID = Form(...),
    caption: str | None = Form(None, max_length=500),
    category: MemoryCategory = Form(MemoryCategory.OTHER),
    db: AsyncSession = Depends(get_db_session),
) -> MemoryResponse:
    payload = MemoryUploadRequest(album_id=album_id, caption=caption, category=category)
    service = MemoryService(db)
    return await service.create_memory(user, payload, file)


@router.get("", response_model=PaginatedResponse[MemoryResponse])
async def list_memories(
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
    album_id: UUID | None = Query(None),
    category: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(30, ge=1, le=100),
) -> PaginatedResponse[MemoryResponse]:
    service = MemoryService(db)
    return await service.list_memories(
        user, album_id=album_id, category=category, page=page, page_size=page_size
    )


@router.get("/{memory_id}", response_model=MemoryResponse)
async def get_memory(
    memory_id: UUID,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> MemoryResponse:
    service = MemoryService(db)
    return await service.get_memory(user, memory_id)


@router.patch("/{memory_id}", response_model=MemoryResponse)
async def update_memory(
    memory_id: UUID,
    payload: MemoryUpdateRequest,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> MemoryResponse:
    service = MemoryService(db)
    return await service.update_memory(user, memory_id, payload)


@router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memory(
    memory_id: UUID,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> None:
    service = MemoryService(db)
    await service.delete_memory(user, memory_id)
