from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.schemas.common import PaginatedResponse
from app.application.schemas.letter import LetterCreateRequest, LetterResponse
from app.application.services.domain_services.letter_service import LetterService
from app.core.dependencies.auth import require_couple
from app.core.dependencies.rate_limit import RateLimit
from app.domain.enums.letter_status import LetterStatus
from app.domain.models.user import User
from app.infra.db.session import get_db_session

router = APIRouter(prefix="/letters", tags=["Letters"])

CoupleUser = Annotated[User, Depends(require_couple)]


@router.post("", response_model=LetterResponse, status_code=status.HTTP_201_CREATED)
async def create_draft(
    payload: LetterCreateRequest,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> LetterResponse:
    service = LetterService(db)
    return await service.create_draft(user, payload)


@router.get("", response_model=PaginatedResponse[LetterResponse])
async def list_letters(
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: LetterStatus | None = Query(None),
    only_received: bool | None = Query(None),
    only_sent: bool | None = Query(None),
) -> PaginatedResponse[LetterResponse]:
    service = LetterService(db)
    return await service.list(
        user,
        page=page,
        page_size=page_size,
        status=status,
        only_received=only_received,
        only_sent=only_sent,
    )


@router.get("/unread/count")
async def unread_count(
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    service = LetterService(db)
    return await service.get_unread_count(user)


@router.get("/{letter_id}", response_model=LetterResponse)
async def get_letter(
    letter_id: UUID,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> LetterResponse:
    service = LetterService(db)
    return await service.get_letter(user, letter_id)


@router.patch("/{letter_id}", response_model=LetterResponse)
async def update_draft(
    letter_id: UUID,
    payload: LetterCreateRequest,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> LetterResponse:
    service = LetterService(db)
    return await service.update_draft(user, letter_id, payload)


@router.delete("/{letter_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_letter(
    letter_id: UUID,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> None:
    service = LetterService(db)
    await service.delete(user, letter_id)


@router.post("/{letter_id}/send", response_model=LetterResponse)
async def send_letter(
    letter_id: UUID,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> LetterResponse:
    service = LetterService(db)
    return await service.send(user, letter_id)


@router.post("/{letter_id}/read", response_model=LetterResponse)
async def read_letter(
    letter_id: UUID,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> LetterResponse:
    service = LetterService(db)
    return await service.mark_read(user, letter_id)