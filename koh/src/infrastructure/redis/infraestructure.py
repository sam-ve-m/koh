import redis.asyncio as aioredis
from koh.src.infrastructure.env_config import config


class RedisInfrastructure:
    redis = None

    @classmethod
    def get_redis(cls):
        if cls.redis is None:
            url = config("KOH_REDIS_HOST_URL")
            cls.redis = aioredis.from_url(url)
        return cls.redis
