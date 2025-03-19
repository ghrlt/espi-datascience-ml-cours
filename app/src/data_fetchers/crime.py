from data_fetchers.base_scraper import Scraper
import pandas as pd
import re

class CrimeScraper(Scraper):
    def parse_data(self, soup):
        data = []
        table = soup.select('table.table_builder_with_value_explanation')[0]
        rows = table.select('tr')

        for row in rows:
            try:
                if row.select('td'):
                    description = row.select('td.columnWithName')[0].text.strip()
                    value = re.sub(r'\n.*', '', row.select('td.indexValueTd')[0].text.strip())
                    data.append((description, value, "%"))
            except Exception as e:
                print(f"Erreur parsing crime : {e}")
        return data

    def get_data(self, urls):
        all_data = []
        for url in urls:
            soup = self.fetch_data(self.base_url + url)
            if soup:
                all_data.extend(self.parse_data(soup))
        return pd.DataFrame(all_data, columns=["description", "value", "unit"])
