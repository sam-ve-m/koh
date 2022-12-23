from typing import Optional
from koh.src.infrastructure.redis.infraestructure import RedisInfrastructure


class CacheRepository:
    prefix = "koh-liveness"

    @classmethod
    async def set(cls, key: str, value: str, ttl: int):
        redis = RedisInfrastructure.get_redis()
        key = ":".join((cls.prefix, key))
        await redis.set(name=key, value=value, ex=ttl)

    @classmethod
    async def get(cls, key: str) -> Optional[str]:
        redis = RedisInfrastructure.get_redis()
        key = ":".join((cls.prefix, key))
        if value := await redis.get(name=key):
            return value.decode()
