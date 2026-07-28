from typing import Annotated
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.schemas.common import PaginatedResponse
from app.application.schemas.surprises import (
    SurpriseCreateRequest,
    SurpriseResponse,
    SurpriseUpdateRequest,
)
from app.application.services.domain_services.surprise_service import SurpriseService
from app.core.dependencies.premium import PremiumUser, require_premium
from app.core.dependencies.rate_limit import RateLimit
from app.domain.enums.surprise_enums import SurpriseStatus, SurpriseType
from app.domain.models.user import User
from app.infra.db.session import get_db_session

router = APIRouter(prefix="/surprises", tags=["Surprises"])

PremiumUser = Annotated[User, Depends(require_premium)]


@router.post("", response_model=SurpriseResponse, status_code=status.HTTP_201_CREATED)
async def create_surprise(
    user: PremiumUser,
    _: RateLimit,
    title: str = Form(...),
    surprise_type: SurpriseType = Form(...),
    message: str | None = Form(None),
    unlocks_at: datetime | None = Form(None),
    media: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db_session),
) -> SurpriseResponse:
    payload = SurpriseCreateRequest(
        title=title,
        message=message,
        surprise_type=surprise_type,
        unlocks_at=unlocks_at,
    )
    service = SurpriseService(db)
    return await service.create(user, payload, media)


@router.get("", response_model=PaginatedResponse[SurpriseResponse])
async def list_surprises(
    user: PremiumUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
    status: SurpriseStatus | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> PaginatedResponse[SurpriseResponse]:
    service = SurpriseService(db)
    return await service.list_surprises(user, status=status, page=page, page_size=page_size)


@router.get("/{surprise_id}", response_model=SurpriseResponse)
async def get_surprise(
    surprise_id: UUID,
    user: PremiumUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> SurpriseResponse:
    service = SurpriseService(db)
    return await service.get_surprise(user, surprise_id)


@router.patch("/{surprise_id}", response_model=SurpriseResponse)
async def update_surprise(
    surprise_id: UUID,
    payload: SurpriseUpdateRequest,
    user: PremiumUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> SurpriseResponse:
    service = SurpriseService(db)
    return await service.update(user, surprise_id, payload)


@router.delete("/{surprise_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_surprise(
    surprise_id: UUID,
    user: PremiumUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> None:
    service = SurpriseService(db)
    await service.delete_surprise(user, surprise_id)


@router.post("/{surprise_id}/open", response_model=SurpriseResponse)
async def open_surprise(
    surprise_id: UUID,
    user: PremiumUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> SurpriseResponse:
    service = SurpriseService(db)
    return await service.open_surprise(user, surprise_id)
