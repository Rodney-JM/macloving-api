import redis.asyncio as aioredis
import json

from typing import Any
from app.infra.cache.client import _key_watch_state

class WatchStateCache:
    TLL = 3600
    
    def __init__(self, redis: aioredis.Redis) -> None:
        self.redis = redis
    
    async def set_state(self, couple_id: str, state: dict[str, Any]) -> None:
        await self.redis.setex(
            _key_watch_state(couple_id), self.TLL, json.dumps(state)
        )
    
    async def get_state(self, couple_id: str) -> dict[str, Any] | None:
        raw = await self.redis.get(_key_watch_state(couple_id))
        return json.loads(raw) if raw else None
    
    async def clear(self, couple_id: str) -> None:
        await self.redis.delete(_key_watch_state(couple_id))