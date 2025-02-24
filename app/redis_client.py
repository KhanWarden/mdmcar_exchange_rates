from redis.asyncio import Redis
import config


redis = Redis.from_url(config.REDIS_URL)


async def save_exchange_rate(key: str, value: float) -> None:
    async with redis.client() as client:
        await client.set(key, value)


async def get_exchange_rate(key: str) -> float:
    async with redis.client() as client:
        value = await client.get(key)
        return float(value) if value else None
