import logging
from datetime import datetime
from typing import Optional

from .currency_parser import CurrencyParser

logging.basicConfig(level=logging.INFO)


class RubParser(CurrencyParser):
    @classmethod
    def get_exchange_rate(cls, rates: dict) -> float:
        usd_to_rub: float = float(rates.get("quotes", {}).get("USDRUB", 0))
        converted_rate = (usd_to_rub * (1 + 3.3 / 100)) + 1.5
        return round(converted_rate, 2)
