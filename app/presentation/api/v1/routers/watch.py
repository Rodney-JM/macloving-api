from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.schemas.common import PaginatedResponse
from app.application.schemas.watch_session import (
    WatchSessionCreateRequest,
    WatchSessionResponse,
)
from app.application.services.domain_services.watch_service import WatchService
from app.core.dependencies.premium import PremiumUser, require_premium
from app.core.dependencies.rate_limit import RateLimit
from app.core.exceptions import NotFoundError
from app.domain.models.user import User
from app.infra.db.session import get_db_session

router = APIRouter(prefix="/watch", tags=["Watch Together"])

PremiumUser = Annotated[User, Depends(require_premium)]


@router.post("", response_model=WatchSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_watch_session(
    payload: WatchSessionCreateRequest,
    user: PremiumUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> WatchSessionResponse:
    service = WatchService(db)
    return await service.create_session(user, payload)


@router.get("", response_model=WatchSessionResponse | None)
async def get_active_session(
    user: PremiumUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> WatchSessionResponse | None:
    service = WatchService(db)
    return await service.get_active(user)


@router.get("/history", response_model=PaginatedResponse[WatchSessionResponse])
async def get_watch_history(
    user: PremiumUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> PaginatedResponse[WatchSessionResponse]:
    service = WatchService(db)
    return await service.get_history(user, page=page, page_size=page_size)


@router.patch("/{session_id}", response_model=WatchSessionResponse)
async def update_watch_session(
    session_id: UUID,
    payload: WatchSessionCreateRequest,
    user: PremiumUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> WatchSessionResponse:
    service = WatchService(db)
    return await service.update_session(user, session_id, payload)


@router.post("/{session_id}/join", response_model=WatchSessionResponse)
async def join_watch_session(
    session_id: UUID,
    user: PremiumUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> WatchSessionResponse:
    service = WatchService(db)
    return await service.join_session(user, session_id)


@router.post("/{session_id}/leave", status_code=status.HTTP_204_NO_CONTENT)
async def leave_watch_session(
    session_id: UUID,
    user: PremiumUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> None:
    service = WatchService(db)
    await service.leave_session(user, session_id)


@router.post("/{session_id}/end", response_model=WatchSessionResponse)
async def end_watch_session(
    session_id: UUID,
    user: PremiumUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> WatchSessionResponse:
    service = WatchService(db)
    return await service.end_session(user, session_id)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_watch_session(
    session_id: UUID,
    user: PremiumUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> None:
    service = WatchService(db)
    await service.delete_session(user, session_id)