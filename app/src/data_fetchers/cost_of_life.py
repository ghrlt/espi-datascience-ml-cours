from data_fetchers.base_scraper import Scraper
import pandas as pd

class CostOfLifeScraper(Scraper):
    def parse_data(self, soup):
        data = []
        table = soup.select("table.data_wide_table")[0]
        for row in table.select("tr"):
            cols = row.select("td")
            if len(cols) > 1:
                data.append((cols[0].text, cols[1].text))
        return data

    def get_data(self, urls):
        all_data = []
        for url in urls:
            soup = self.fetch_data(self.base_url + url)
            if soup:
                all_data.extend(self.parse_data(soup))
        return pd.DataFrame(all_data, columns=["description", "value"])
