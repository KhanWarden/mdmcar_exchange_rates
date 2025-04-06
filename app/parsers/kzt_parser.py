import logging
from types import NoneType

from .currency_parser import CurrencyParser

logging.basicConfig(level=logging.INFO)


class KZTParser(CurrencyParser):
    HALYK_BANK_URL = "https://back.halykbank.kz/common/currency-history"

    @classmethod
    def get_exchange_rate(cls, rates) -> float:
        data = cls.fetch_json(cls.HALYK_BANK_URL)
        history = data.get("data", {}).get("currencyHistory", {})

        normalized_history = {
            str(k): v for k, v in history.items()
        }

        for key in sorted(normalized_history.keys(), key=int):
            try:
                usd_kzt = normalized_history[key]["privatePersons"]["USD/KZT"]
                sell_rate = float(usd_kzt["sell"])
                return sell_rate
            except (KeyError, TypeError, ValueError):
                logging.warning(f"[HalykBank] Нет данных по ключу '{key}'")
                continue

        logging.error("[HalykBank] Не удалось получить курс USD/KZT")
        raise ValueError("Данные о курсе отсутствуют")
