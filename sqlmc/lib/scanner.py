import aiohttp
import asyncio
import logging
from datetime import datetime
from sqlmc.lib.error import Checker
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

class Scanner(Checker):
    def __init__(self, url, depth):
        super().__init__()
        self.url = url
        self.depth = depth
        self.target_urls = []
        self.web_server = None
        asyncio.run(self.scan(url, depth))

    async def get_server(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                return response.headers.get('Server', 'Unknown')

    async def test_for_sql_injection(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url + "'") as response:
                return self.check(await response.text())

    async def fetch_html(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    async def scan(self, url, depth):
        if depth == 0:
            return
        try:
            html = await self.fetch_html(url)
            soup = BeautifulSoup(html, 'html.parser')
            tasks = []
            for link in soup.find_all('a'):
                href = link.get('href')
                if href is not None:
                    if href.startswith('http'):
                        href = href
                    else:
                        href = self.url + href
                    if href.startswith('/'):
                        href = self.url + href
                    if self.url in href and href not in self.target_urls:
                        tasks.append(self.scan_single_link(href, depth))
            if tasks:
                await asyncio.gather(*tasks)
        except aiohttp.ClientError:
            pass

    async def scan_single_link(self, href, depth):
        vulnerable, db = await self.test_for_sql_injection(href)
        logger.info(f"[{datetime.now()}] Scanned: {href}, Vulnerable: {vulnerable}, Database: {db}")
        self.target_urls.append({
            'url': href,
            'server': await self.get_server(),
            'depth': self.depth - depth,
            'vulnerable': (Color.GREEN + 'Vulnerable' + Color.RESET) if vulnerable else (Color.RED + 'Not Vulnerable' + Color.RESET),
            'db server': (Color.YELLOW + db + Color.RESET) if db else 'N/A'
        })
        await self.scan(href, depth - 1)

    def get_urls(self):
        return self.target_urls
