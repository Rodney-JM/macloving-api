import redis.asyncio as aioredis

from app.infra.cache.client import _key_mood

class MoodCache:
    TLL = 86_400
    
    def __init__(self, redis: aioredis.Redis) -> None:
        self.redis = redis
        
    async def set(self, user_id: str, mood: str) -> None:
        await self.redis.setex(_key_mood(user_id), self.TLL, mood)
        
    async def get(self, user_id: str) -> str | None:
        return await self.redis.get(_key_mood(user_id))
    
    async def delete(self, user_id: str) -> None:
        await self.redis.delete(_key_mood(user_id))
    