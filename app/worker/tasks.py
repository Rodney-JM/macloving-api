import asyncio
from datetime import datetime, timedelta, timezone

from app.core.logging_config import get_logger
from app.domain.enums.subscription_status import SubscriptionStatus

logger = get_logger(__name__)

def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)

def get_celery():
    from app.worker.celery_app import celery_app
    return celery_app


def check_expired_subscriptions():
    async def _inner():
        from app.infra.db.session import _get_session_factory
        from app.infra.repositories.subscription_repo import SubscriptionRepository
        
        now = datetime.now(timezone.utc)
        
        cutoff = now - timedelta(hours=24)
        
        async with _get_session_factory()() as db:
            repo = SubscriptionRepository(db)
            expiring = await repo.get_expiring_soon(cutoff)
            count = 0
            for sub in expiring:
                sub.status = SubscriptionStatus.UNPAID
                count += 1
            await db.commit()
            if count:
                logger.warning("subscriptions_expired_by_task", count=count)
            
    _run(_inner())


def unlock_due_surprises():
    async def _inner():
        from app.infra.db.session import _get_session_factory
        from app.domain.models.session_models.surprise import Surprise, SurpriseStatus
        from sqlalchemy import select
        
        now = datetime.now(timezone.utc)
        async with _get_session_factory()() as db:
            r = await db.execute(
                select(Surprise).where(
                    Surprise.status == SurpriseStatus.LOCKED,
                    Surprise.unlocks_at <= now
                )
            )
            
            surprises = r.scalars().all()
            for s in surprises:
                s.status  = SurpriseStatus.DELIVERED
            await db.commit()
            if surprises:
                logger.info("surprises_unlocked", count=len(surprises))
    
    _run(_inner())

def cleanup_expired_tokens():
    async def _inner():
        from app.infra.db.session import _get_session_factory
        from app.domain.models.couple_models.refresh_token import RefreshToken
        from sqlalchemy import delete
        
        now = datetime.now(timezone.utc)
        async with _get_session_factory()() as db:
            result = await db.execute(
                delete(RefreshToken).where(
                    (RefreshToken.expires_at < now) |
                    (RefreshToken.revoked == True)
                )
            )
            await db.commit()
            logger.info("tokens_cleaned", deleted=result.rowcount)
    
    _run(_inner())