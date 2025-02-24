import asyncio
import config
from parsers import RubParser, WonParser, KZTParser
from redis_client import save_exchange_rate


class Scheduler:
    @classmethod
    async def fetch_and_update_exchange_rate(cls) -> None:
        rub: float = await RubParser.get_usd_to_rub_exchange_rate()
        won: float = await WonParser.get_usd_to_won_exchange_rate()
        kzt: float = await KZTParser.get_usd_to_kzt_exchange_rate()

        if rub:
            await save_exchange_rate(config.REDIS_KEY_RUB, rub)
        if won:
            await save_exchange_rate(config.REDIS_KEY_WON, won)
        if kzt:
            await save_exchange_rate(config.REDIS_KEY_KZT, kzt)

    @classmethod
    async def run_scheduler(cls) -> None:
        while True:
            await cls.fetch_and_update_exchange_rate()
            await asyncio.sleep(config.FETCH_INTERVAL_HOURS * 3600)  # Ждем 8 часов
