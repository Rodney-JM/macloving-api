from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.schemas.common import PaginatedResponse
from app.application.schemas.special_dates import (
    SpecialDateCreateRequest,
    SpecialDateResponse,
    SpecialDateUpdateRequest,
)
from app.application.services.domain_services.special_date_service import SpecialDateService
from app.core.dependencies.auth import require_couple
from app.core.dependencies.rate_limit import RateLimit
from app.domain.models.user import User
from app.infra.db.session import get_db_session

router = APIRouter(prefix="/special-dates", tags=["Special Dates"])

CoupleUser = Annotated[User, Depends(require_couple)]


@router.post("", response_model=SpecialDateResponse, status_code=status.HTTP_201_CREATED)
async def create_special_date(
    payload: SpecialDateCreateRequest,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> SpecialDateResponse:
    service = SpecialDateService(db)
    return await service.create_special_date(user, payload)


@router.get("", response_model=PaginatedResponse[SpecialDateResponse])
async def list_special_dates(
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    upcoming_only: bool | None = Query(None),
    recurring_only: bool | None = Query(None),
) -> PaginatedResponse[SpecialDateResponse]:
    service = SpecialDateService(db)
    return await service.list_special_dates(
        user,
        page=page,
        page_size=page_size,
        upcoming_only=upcoming_only,
        recurring_only=recurring_only,
    )


@router.get("/{date_id}", response_model=SpecialDateResponse)
async def get_special_date(
    date_id: UUID,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> SpecialDateResponse:
    service = SpecialDateService(db)
    return await service.get_special_date(user, date_id)


@router.patch("/{date_id}", response_model=SpecialDateResponse)
async def update_special_date(
    date_id: UUID,
    payload: SpecialDateUpdateRequest,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> SpecialDateResponse:
    service = SpecialDateService(db)
    return await service.update_special_date(user, date_id, payload)


@router.delete("/{date_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_special_date(
    date_id: UUID,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> None:
    service = SpecialDateService(db)
    await service.delete_special_date(user, date_id)