import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional

class WebCrawlerBase:
    """Base class for web crawlers."""

    @property
    def headers(self) -> Dict[str, str]:
        """Return default headers for requests."""
        return {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }


class WebCrawlerStockVolumes(WebCrawlerBase):
    """Crawler to fetch stock volumes based on stock ID."""

    def __init__(self, stock_id: str) -> None:
        self.stock_id = stock_id

    @property
    def url(self) -> str:
        """Return the URL to fetch stock volumes."""
        return "https://stock.wespai.com/p/21965"

    def get_volumes(self) -> Optional[str]:
        """Fetch and return the stock volume for the specified stock ID."""
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching stock volumes: {e}")
            return None

        soup = BeautifulSoup(response.text, "html5lib")
        tags = soup.find_all('td')

        for tag in tags:
            if self.stock_id in tag.text and len(tag.text) == 4:
                next_tags = tag.find_next_siblings('td', limit=3)
                if next_tags:
                    return next_tags[-1].text
        return None


class WebCrawlerStockPercentage(WebCrawlerBase):
    """Crawler to fetch stock percentage changes."""

    @property
    def url(self) -> str:
        """Return the URL to fetch stock percentage changes."""
        return "https://www.taifex.com.tw/cht/9/futuresQADetail"

    def get_stock_percentage(self) -> Optional[List[Dict[str, float]]]:
        """Fetch and return a list of stock percentage changes."""
        try:
            response = requests.get(self.url, headers=self.headers)
            response.encoding = 'utf-8'
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching stock percentages: {e}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')

        if table is None:
            print("No table found in the response.")
            return None

        stock_info = []

        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) > 3:
                code = cols[1].text.strip()
                name = cols[2].text.strip()
                percent = cols[3].text.strip()
                try:
                    percent_float = round(float(percent.replace('%', '').replace(',', '')) / 100, 6)
                except ValueError:
                    percent_float = 0.0
                stock_info.append({'code': code, 'name': name, 'percent': percent_float})

        return stock_info
