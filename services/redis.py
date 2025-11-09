from datetime import timedelta

import redis.asyncio as redis

from bot import bot
from core import config

redis_client = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    password=config.REDIS_PASSWORD or None,
    db=0,
    decode_responses=True
)


class BaseRepository:
    TTL = int(timedelta(days=3).total_seconds())
    NAME = str(bot.id)
    PREFIX = "base"

    @classmethod
    def _build_key(cls, *parts: str):
        return f"{cls.NAME}:{cls.PREFIX}:{':'.join(parts)}"

    @classmethod
    async def set(cls, key_part: str, value: str, ttl: int = None) -> None:
        full_key = cls._build_key(key_part)
        ttl = ttl if ttl is not None else cls.TTL
        await redis_client.setex(full_key, ttl, value)

    @classmethod
    async def get(cls, key_part: str) -> str | None:
        full_key = cls._build_key(key_part)
        return await redis_client.get(full_key)

    @classmethod
    async def exists(cls, key_part: str) -> bool:
        full_key = cls._build_key(key_part)
        return bool(await redis_client.exists(full_key))

    @classmethod
    async def delete(cls, key_part: str) -> int:
        full_key = cls._build_key(key_part)
        return await redis_client.delete(full_key)
