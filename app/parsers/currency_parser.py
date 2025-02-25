import logging
import requests
from abc import ABC, abstractmethod
from xml.etree import ElementTree as ET

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class CurrencyParser(ABC):
    headers = {"User-Agent": "Mozilla/5.0"}

    @classmethod
    @abstractmethod
    def get_exchange_rate(cls) -> float:
        pass

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
