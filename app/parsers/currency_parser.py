import os
import logging
from typing import Optional

import requests
from abc import ABC, abstractmethod
from xml.etree import ElementTree as ET
from dotenv import load_dotenv


load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class CurrencyParser(ABC):
    headers = {"User-Agent": "Mozilla/5.0"}
    API_KEY = os.getenv("API_KEY")

    @classmethod
    @abstractmethod
    def get_exchange_rate(cls, currency_rates: dict | None) -> float:
        pass

    @classmethod
    def get_currency_rates(cls) -> dict:
        try:
            api_url: str = f"https://api.currencylayer.com/live?access_key={cls.API_KEY}"
            rates = cls.fetch_json(api_url)
            if not rates.get("success"):
                raise logging.error(f"Ошибка API: {rates.get('error', {}).get('info', 'Неизвестная ошибка')}")
            return rates
        except Exception as e:
            logging.exception("Ошибка при получении курсов валют")
            raise

    @classmethod
    def fetch_json(cls, url: str) -> dict:
        try:
            response = requests.get(url, headers=cls.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Ошибка запроса {url}: {e}")

    @classmethod
    def fetch_xml(cls, url: str) -> ET.Element:
        try:
            response = requests.get(url, headers=cls.headers)
            response.raise_for_status()
            return ET.fromstring(response.text)
        except requests.RequestException as e:
            logging.error(f"Ошибка запроса {url}: {e}")
