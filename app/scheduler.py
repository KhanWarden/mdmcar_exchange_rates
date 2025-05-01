import asyncio
import time
import logging

from app.parsers import WonParser, RubParser, KZTParser, CurrencyParser
from app.redis_client import save_exchange_rate


logging.basicConfig(level=logging.INFO)


async def fetch_and_update_exchange_rate():
    logging.info("Updating exchange rates")
    currency_rates = CurrencyParser.get_currency_rates()

    async def get_won_rate():
        return await WonParser.get_exchange_rate()

    parsers = {
        "usd_to_rub_rate": lambda: RubParser.get_exchange_rate(currency_rates),
        "usd_to_kzt_rate": lambda: KZTParser.get_exchange_rate(currency_rates),
        "usd_to_won_rate": get_won_rate,
    }

    for redis_key, get_rate in parsers.items():
        try:
            if asyncio.iscoroutinefunction(get_rate):
                rate = await get_rate()
            else:
                rate = get_rate()
            logging.info(f"{redis_key}: {rate}")
            save_exchange_rate(redis_key, rate)
        except Exception:
            logging.error(f"[Error] Не удалось получить курс для {redis_key}")


async def run_scheduler():
    while True:
        await fetch_and_update_exchange_rate()
        seconds = get_random_sleep_time()
        logging.info(f"Waiting for next fetch in {seconds} seconds")
        await asyncio.sleep(seconds)


def get_random_sleep_time() -> int:
    import random
    return random.randint(3600, 10800)
