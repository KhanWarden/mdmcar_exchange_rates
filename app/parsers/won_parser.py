import logging

from .currency_parser import CurrencyParser


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class WonParser(CurrencyParser):
    API_URL = "https://api.currencylayer.com/live"

    @classmethod
    def get_exchange_rate(cls, rates: dict) -> float:
        usd_to_krw = float(rates.get("quotes", {}).get("USDKRW", 0))
        converted_rate = usd_to_krw + 5
        return round(converted_rate, 2)
