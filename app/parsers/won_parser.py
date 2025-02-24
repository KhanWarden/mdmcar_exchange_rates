import logging
import os

import aiohttp
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
load_dotenv()

API_KEY = os.getenv('API_KEY')


class WonParser:
    @staticmethod
    async def get_usd_to_won_exchange_rate() -> float | None:
        url = f"https://api.currencylayer.com/live?access_key={API_KEY}"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        logging.error(f"Ошибка запроса {response.status}: {url}")
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status
                        )

                    data = await response.json()
                    if not data.get("success"):
                        raise f"Ошибка API: {data.get('error', {}).get('info', 'Неизвестная ошибка')}"

                    usd_to_krw = data.get("quotes", {}).get("USDKRW")

                    if usd_to_krw:
                        print(usd_to_krw)
                        needed_rate = float(usd_to_krw) * 0.99024 - 10
                        return round(needed_rate, 2)
                    else:
                        raise "Не удалось получить курсы валют"

        except Exception as e:
            logging.error(f"Ошибка при получении курса: {e}")
