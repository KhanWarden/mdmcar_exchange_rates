import logging
import requests

from .currency_parser import CurrencyParser

logging.basicConfig(level=logging.INFO)


class RubParser(CurrencyParser):
    @classmethod
    def get_exchange_rate(cls, rates: dict = None) -> float:
        api_url = "https://api-app.sovcombank.ru/v1/currency/7700000000000"
        response = requests.get(api_url)
        json = response.json()
        usd_to_rub = float(json.get("usd").get("buy"))
        converted_rate = usd_to_rub + 2
        return round(converted_rate, 2)
