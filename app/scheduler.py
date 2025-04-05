import time
import logging

from app.parsers import WonParser, RubParser, KZTParser, CurrencyParser
from app.redis_client import save_exchange_rate


logging.basicConfig(level=logging.INFO)


def fetch_and_update_exchange_rate():
    logging.info("Updating exchange rates")
    currency_rates = CurrencyParser.get_currency_rates()
    parsers = {
        "usd_to_rub_rate": RubParser.get_exchange_rate(currency_rates),
        "usd_to_kzt_rate": KZTParser.get_exchange_rate(rates=None),
        "usd_to_won_rate": WonParser.get_exchange_rate(currency_rates),
    }

    for redis_key, parser in parsers.items():
        rate = parser
        logging.info(f"{redis_key}: {rate}")
        save_exchange_rate(redis_key, rate)


def run_scheduler():
    hours = 1
    while True:
        fetch_and_update_exchange_rate()
        logging.info("Waiting for next fetch")
        time.sleep(3600 * hours)
