from typing import Optional
from mnemosine import AsyncCache

class CacheRepository:
    prefix = "koh-liveness"

    @classmethod
    async def set(cls, key: str, value: str, ttl: int):
        key = ":".join((cls.prefix, key))
        await AsyncCache.save(key=key, value=value, time_to_live=ttl)

    @classmethod
    async def get(cls, key: str) -> Optional[str]:
        key = ":".join((cls.prefix, key))
        value = await AsyncCache.get(key=key)
        return value
