from bs4 import BeautifulSoup
import requests

class WebCrawlerStockVolumes:

    def __init__(self, stock_id:str) -> None:
        self.stock_id = stock_id
        
    @property
    def get_url(self) -> str:
        return "https://stock.wespai.com/p/21965"

    @property
    def get_header(self) -> str:
        return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }

    def get_volumes(self):
        response = requests.get(self.get_url, headers=self.get_header)
        soup = BeautifulSoup(response.text, "html5lib")
        tags = soup.find_all('td')
        for tag in tags:
            if self.stock_id in tag.text and len(tag.text) == 4:
                next_tags = tag.find_next_siblings('td', limit=3)
                return next_tags[-1].text

