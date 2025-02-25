import logging
from datetime import datetime
from .currency_parser import CurrencyParser

logging.basicConfig(level=logging.INFO)


class RubParser(CurrencyParser):
    CBR_URL = "https://www.cbr.ru/scripts/XML_daily.asp"
    USD_RUB_ID = "R01235"  # ID доллара

    @classmethod
    def get_exchange_rate(cls) -> float:
        formatted_date = datetime.now().strftime("%d/%m/%Y")
        url = f"{cls.CBR_URL}?date_req={formatted_date}"
        data = cls.fetch_xml(url)

        if data is None:
            raise "Failed to fetch data"

        for valute in data.findall("Valute"):
            if valute.get("ID") == cls.USD_RUB_ID:
                value: float = float(valute.find("Value").text.replace(",", "."))

                return round(value - 0.1, 2)
