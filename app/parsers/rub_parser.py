import logging
from datetime import datetime
from typing import Optional

from .currency_parser import CurrencyParser

logging.basicConfig(level=logging.INFO)


class RubParser(CurrencyParser):
    CBR_URL = "https://www.cbr.ru/scripts/XML_daily.asp"
    USD_RUB_ID = "R01235"  # ID доллара

    # @classmethod
    # def get_exchange_rate(cls, rates: dict) -> float:
    #     formatted_date = datetime.now().strftime("%d/%m/%Y")
    #     url = f"{cls.CBR_URL}?date_req={formatted_date}"
    #     data = cls.fetch_xml(url)
    #
    #     if data is None:
    #         raise "Failed to fetch data"
    #
    #     for valute in data.findall("Valute"):
    #         if valute.get("ID") == cls.USD_RUB_ID:
    #             value: float = float(valute.find("Value").text.replace(",", "."))
    #
    #             return round(value * 1.045, 2)

    @classmethod
    def get_exchange_rate(cls, rates: dict) -> float:
        usd_to_rub: float = float(rates.get("quotes", {}).get("USDRUB", 0))
        converted_rate = usd_to_rub * (1 + 3.3 / 100)
        return round(converted_rate, 2)
