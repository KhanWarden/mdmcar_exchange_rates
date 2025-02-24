import logging
from datetime import datetime
from xml.etree import ElementTree as ET
import aiohttp

logging.basicConfig(level=logging.INFO)


class RubParser:
    CBR_URL = "https://cbr.ru/scripts/XML_daily.asp"
    USD_RUB_ID = "R01235"  # ID доллара

    @classmethod
    async def get_usd_to_rub_exchange_rate(cls) -> float:
        """ Получает курс USD/RUB с сайта ЦБ РФ """
        formatted_date = datetime.now().strftime("%d/%m/%Y")
        url = f"{cls.CBR_URL}?date_req={formatted_date}"
        headers = {"User-Agent": "Mozilla/5.0"}
        async with aiohttp.ClientSession(headers=headers) as session:
            try:
                async with session.get(url) as response:
                    if response.status != 200:
                        logging.error(f"Ошибка запроса {response.status}: {url}")
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status
                        )

                    xml_content = await response.text()
                    root = ET.fromstring(xml_content)

                    for valute in root.findall("Valute"):
                        if valute.get("ID") == cls.USD_RUB_ID:
                            value = valute.find("Value").text.replace(",", ".")
                            return float(value)
            except Exception as e:
                logging.error(f"Ошибка при получении курса: {e}")
