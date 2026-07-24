from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.schemas.common import PaginatedResponse
from app.application.schemas.rituals import (
    RitualCreateRequest,
    RitualEntryRequest,
    RitualResponse,
    RitualUpdateRequest,
    RitualWithStatusResponse,
)
from app.application.services.domain_services.ritual_service import RitualService
from app.core.dependencies.auth import require_couple
from app.core.dependencies.rate_limit import RateLimit
from app.domain.enums.ritual_status import RitualStatus
from app.domain.models.user import User
from app.infra.db.session import get_db_session

router = APIRouter(prefix="/rituals", tags=["Rituals"])

CoupleUser = Annotated[User, Depends(require_couple)]


@router.post("", response_model=RitualResponse, status_code=status.HTTP_201_CREATED)
async def create_ritual(
    payload: RitualCreateRequest,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> RitualResponse:
    service = RitualService(db)
    return await service.create_ritual(user, payload)


@router.get("", response_model=PaginatedResponse[RitualResponse])
async def list_rituals(
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
    only_active: bool = Query(True),
    page: int = Query(1, ge=1),
    page_size: int = Query(30, ge=1, le=100),
) -> PaginatedResponse[RitualResponse]:
    service = RitualService(db)
    return await service.list_rituals(user, only_active=only_active, page=page, page_size=page_size)


@router.get("/{ritual_id}", response_model=RitualResponse)
async def get_ritual(
    ritual_id: UUID,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> RitualResponse:
    service = RitualService(db)
    return await service.get_ritual(user, ritual_id)


@router.patch("/{ritual_id}", response_model=RitualResponse)
async def update_ritual(
    ritual_id: UUID,
    payload: RitualUpdateRequest,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> RitualResponse:
    service = RitualService(db)
    return await service.update_ritual(user, ritual_id, payload)


@router.delete("/{ritual_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ritual(
    ritual_id: UUID,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> None:
    service = RitualService(db)
    await service.delete_ritual(user, ritual_id)


@router.post("/{ritual_id}/complete", response_model=RitualWithStatusResponse)
async def complete_ritual(
    ritual_id: UUID,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> RitualWithStatusResponse:
    service = RitualService(db)
    payload = RitualEntryRequest(status=RitualStatus.COMPLETED)
    return await service.record_entry(user, ritual_id, payload)


@router.post("/{ritual_id}/skip", response_model=RitualWithStatusResponse)
async def skip_ritual(
    ritual_id: UUID,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> RitualWithStatusResponse:
    service = RitualService(db)
    payload = RitualEntryRequest(status=RitualStatus.SKIPPED)
    return await service.record_entry(user, ritual_id, payload)
