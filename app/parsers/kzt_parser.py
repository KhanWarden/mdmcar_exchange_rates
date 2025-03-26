import logging
from types import NoneType

from .currency_parser import CurrencyParser

logging.basicConfig(level=logging.INFO)


class KZTParser(CurrencyParser):
    HALYK_BANK_URL = "https://back.halykbank.kz/common/currency-history"

    @classmethod
    def get_exchange_rate(cls) -> float:
        data = cls.fetch_json(cls.HALYK_BANK_URL)

        try:
            usd_kzt_sell = data["data"]["currencyHistory"][0]["privatePersons"]["USD/KZT"]["sell"]
            return float(usd_kzt_sell)
        except (KeyError, TypeError):
            usd_kzt_sell = data["data"]["currencyHistory"]["0"]["privatePersons"]["USD/KZT"]["sell"]
            return usd_kzt_sell
        except:
            logging.error("Ошибка парсинга данных Halyk Bank")
            raise
