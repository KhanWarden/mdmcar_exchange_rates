import logging

import aiohttp
import requests
from bs4 import BeautifulSoup

from currency_parser import CurrencyParser


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")



class WonParser(CurrencyParser):
    url = "https://m.search.naver.com/search.naver?sm=mtb_sly.hst&where=m&ssc=tab.m.all&oquery=%ED%99%98%EC%9C%A8&tqi=iyxtplprc%2B0ssQjWSfGssssssWG-247280&query=%ED%85%8C%EB%8D%94&acr=2"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    }
    _proxy = "http://mdmcarcom:oWGUK9kK42BRAJ@s6.airproxy.io:20401"
    proxy = {"http": _proxy,
             "https": _proxy}

    @classmethod
    async def get_exchange_rate(cls, rates: dict = None) -> float:
        async with aiohttp.ClientSession() as session:
            async with session.get(cls.url, headers=cls.headers, proxy=cls._proxy) as response:
                print("Status:", response.status)
                page_content = await response.text()
                soup = BeautifulSoup(page_content, "html.parser")
                price_tag = soup.select_one('strong.price em')
                if price_tag:
                    currency_rate = price_tag.text.strip().replace(",", "")
                    return float(currency_rate)
                else:
                    raise Exception("No price tag found")

