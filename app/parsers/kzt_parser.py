import logging

from .currency_parser import CurrencyParser

logging.basicConfig(level=logging.INFO)


class KZTParser(CurrencyParser):
    HALYK_BANK_URL = "https://back.halykbank.kz/common/currency-history"

    @classmethod
    def get_exchange_rate(cls, rates) -> float:
        usd_to_kzt: float = float(rates.get("quotes", {}).get("USDKZT", 0))
        return round(usd_to_kzt, 2)
