from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.schemas.mood import MoodUpdateRequest, MoodResponse
from app.application.services.domain_services.mood_service import MoodService
from app.core.dependencies.auth import require_couple
from app.core.dependencies.rate_limit import RateLimit
from app.domain.enums.mood_type import MoodType
from app.domain.models.user import User
from app.infra.cache.client import get_redis
from app.infra.db.session import get_db_session
from app.presentation.websockets.manager import ws_manager

router = APIRouter(prefix="/mood", tags=["Mood"])

CoupleUser = Annotated[User, Depends(require_couple)]


class CoupleMoodResponse(BaseModel):
    user_mood: MoodType | None
    user_updated_at: datetime | None
    partner_mood: MoodType | None
    partner_updated_at: datetime | None


@router.put("", response_model=MoodResponse)
async def update_mood(
    payload: MoodUpdateRequest,
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
    redis=Depends(get_redis),
) -> MoodResponse:
    service = MoodService(db, redis)
    return await service.update(user, payload, ws_manager)


@router.get("", response_model=CoupleMoodResponse)
async def get_moods(
    user: CoupleUser,
    _: RateLimit,
    db: AsyncSession = Depends(get_db_session),
    redis=Depends(get_redis),
) -> CoupleMoodResponse:
    service = MoodService(db, redis)
    partner_mood = await service.get_partner_mood(user)
    return CoupleMoodResponse(
        user_mood=user.current_mood,
        user_updated_at=user.mood_updated_at,
        partner_mood=partner_mood.mood if partner_mood else None,
        partner_updated_at=partner_mood.updated_at if partner_mood else None,
    )