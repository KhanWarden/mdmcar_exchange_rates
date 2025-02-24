import logging
import aiohttp


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class KZTParser:
    HALYK_BANK_URL = "https://back.halykbank.kz/common/currency-history"

    @classmethod
    async def get_usd_to_kzt_exchange_rate(cls) -> float:
        headers = {"User-Agent": "Mozilla/5.0"}
        async with aiohttp.ClientSession(headers=headers) as session:
            try:
                async with session.get(cls.HALYK_BANK_URL) as response:
                    if response.status != 200:
                        logging.error(f"Ошибка запроса {response.status}: {cls.HALYK_BANK_URL}")
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status
                        )

                    data = await response.json()
                    usd_kzt_sell = data["data"]["currencyHistory"]["1"]["privatePersons"]["USD/KZT"]["sell"]
                    return float(usd_kzt_sell)

            except Exception as e:
                logging.error(f"Ошибка при получении курса: {e}")
