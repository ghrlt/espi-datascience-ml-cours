import requests
from bs4 import BeautifulSoup
import time

class Scraper:
    def __init__(self, base_url, sleep=0.2):
        self.base_url = base_url
        self.sleep = sleep

    def fetch_data(self, url):
        time.sleep(self.sleep)
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.RequestException as e:
            print(f"Erreur lors de la récupération de {url} : {e}")
            if response.status_code == 429:
                print("429 Too Many Requests. Exitting...")
                exit(429)

            return None

    def parse_data(self, soup):
        raise NotImplementedError
    
    def get_data(self, urls):
        raise NotImplementedError