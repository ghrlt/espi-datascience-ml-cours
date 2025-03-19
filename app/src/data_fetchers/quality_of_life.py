from data_fetchers.base_scraper import Scraper
import pandas as pd
import re

class QualityOfLifeScraper(Scraper):
    def parse_data(self, soup):
        data = []
        table = soup.select('table')[2]  # On prend le bon tableau
        rows = table.select('tr')

        for row in rows:
            try:
                if row.select('a.discreet_link') and not row.select('a.hide_smaller_than_600'):
                    description = row.select('a.discreet_link')[0].text.strip()
                    value = row.select('td')[1].text.strip()
                    data.append((description, value, "%"))
            except Exception as e:
                print(f"Erreur parsing qualité de vie : {e}")
        return data

    def get_data(self, urls):
        all_data = []
        for url in urls:
            soup = self.fetch_data(self.base_url + url)
            if soup:
                all_data.extend(self.parse_data(soup))
        return pd.DataFrame(all_data, columns=["description", "value", "unit"])
