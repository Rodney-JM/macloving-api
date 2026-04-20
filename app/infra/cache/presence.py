import redis.asyncio as aioredis

from app.infra.cache.client import _key_online

class PresenceService:
    ONLINE_TTL = 90
    
    def __init__(self, redis: aioredis.Redis) -> None:
        self.redis = redis
        
    async def set_online(self, user_id: str) -> None:
        await self.redis.setex(_key_online(user_id), self.ONLINE_TTL, "1")
    
    async def set_offline(self, user_id: str) -> None:
        await self.redis.delete(_key_online(user_id))
    
    async def is_online(self, user_id: str) -> bool:
        return bool(await self.redis.exists(_key_online(user_id)))