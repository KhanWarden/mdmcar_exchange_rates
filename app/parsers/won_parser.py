import logging
import os

from dotenv import load_dotenv

from .currency_parser import CurrencyParser


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()
API_KEY = os.getenv("API_KEY")


class WonParser(CurrencyParser):
    API_URL = "https://api.currencylayer.com/live"

    @classmethod
    def get_exchange_rate(cls) -> float:
        if not API_KEY:
            raise logging.error("API_KEY не найден в .env")

        url = f"{cls.API_URL}?access_key={API_KEY}"
        data = cls.fetch_json(url)

        if not data.get("success"):
            raise logging.error(f"Ошибка API: {data.get('error', {}).get('info', 'Неизвестная ошибка')}")

        usd_to_krw = data.get("quotes", {}).get("USDKRW", 0)
        converted_rate = usd_to_krw * 0.99024 - 10  # Rate for sale
        return round(converted_rate, 2)
