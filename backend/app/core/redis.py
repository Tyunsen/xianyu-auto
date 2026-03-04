import redis.asyncio as aioredis
from app.core.config import get_settings

settings = get_settings()


class RedisClient:
    _instance = None
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = aioredis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
        return cls._client

    @classmethod
    async def close(cls):
        if cls._client:
            await cls._client.close()
            cls._client = None


def get_redis():
    """获取Redis客户端"""
    return RedisClient.get_client()
