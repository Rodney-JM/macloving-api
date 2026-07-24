from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.schemas.album import AlbumCreate, AlbumResponse, AlbumUpdate
from app.application.schemas.common import PaginatedResponse
from app.application.services.domain_services.album_service import AlbumService
from app.core.dependencies.auth import require_couple
from app.core.dependencies.rate_limit import RateLimit
from app.domain.models.user import User
from app.infra.db.session import get_db_session

router = APIRouter(prefix="/albums", tags=["Albums"])

CoupleUser = Annotated[User, Depends(require_couple)]


@router.post("", response_model=AlbumResponse, status_code=status.HTTP_201_CREATED)
async def create_album(
    payload: AlbumCreate,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> AlbumResponse:
    service = AlbumService(db)
    return await service.create_album(user, payload)


@router.get("", response_model=PaginatedResponse[AlbumResponse])
async def list_albums(
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
    page: int = Query(1, ge=1),
    page_size: int = Query(30, ge=1, le=100),
) -> PaginatedResponse[AlbumResponse]:
    service = AlbumService(db)
    return await service.list_albums(user, page=page, page_size=page_size)


@router.patch("/{album_id}", response_model=AlbumResponse)
async def update_album(
    album_id: UUID,
    payload: AlbumUpdate,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> AlbumResponse:
    service = AlbumService(db)
    return await service.update_album(user, album_id, payload)


@router.delete("/{album_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_album(
    album_id: UUID,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
) -> None:
    service = AlbumService(db)
    await service.delete_album(user, album_id)
