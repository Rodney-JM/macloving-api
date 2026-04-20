import json
import redis.asyncio as aioredis

from typing import Any
from app.core.config import settings
from app.infra.cache.client import _key_cache

class QueryCache:
    def __init__(self, redis: aioredis.Redis, ttl: int = settings.REDIS_CACHE_TTL) -> None:
        self.redis = redis
        self.ttl = ttl
        
    async def get(self, namespace: str, key: str) -> Any | None:
        raw = await self.redis.get(_key_cache(namespace, key))
        return json.loads(raw) if raw else None
    
    async def set(self, namespace: str, key: str, value: Any) -> None:
        await self.redis.setex(_key_cache(namespace, key), self.ttl, json.dumps(value))
    
    async def invalidate(self, namespace: str, key: str) -> None:
        await self.redis.delete(_key_cache(namespace, key))
    
    async def invalidate_namespace(self, namespace: str) -> None:
        pattern = _key_cache(namespace, "*")
        keys = await self.redis.keys(pattern)
        if keys:
            await self.redis.delete(*keys)