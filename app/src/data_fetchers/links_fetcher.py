import requests
import pandas as pd
from bs4 import BeautifulSoup
from db.repository import Repository

class LinksFetcher:
    BASE_URL = "https://www.numbeo.com/cost-of-living/"

    def fetch_links(self):
        """
        Fetches country links from Numbeo's cost of living page.
        Returns a DataFrame with country names and their respective links.
        """
        print("🔍 Fetching country links...")
        response = requests.get(self.BASE_URL)

        if response.status_code != 200:
            print(f"❌ Error fetching {self.BASE_URL}: {response.status_code}")
            return pd.DataFrame()

        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.select('table.related_links')

        countries = []
        links = []

        for table in tables:
            for anchor in table.select('a'):
                country = anchor.text.strip()
                country_link = anchor['href']

                countries.append(country)
                links.append(country_link)

        df = pd.DataFrame({'country': countries, 'country_link': links})

        print(f"✅ Fetched {len(df)} country links!")
        return df

    def store_links(self, df):
        """
        Stores country links into the PostgreSQL database.
        """
        if df.empty:
            print("⚠️ No country links to insert.")
            return

        repo = Repository()
        print("🗄 Inserting country links into the database...")
        repo.insert_data("links", df)
        repo.close()
        print("✅ Country links inserted successfully!")

    def run(self):
        """
        Fetches and stores country links.
        """
        df = self.fetch_links()
        self.store_links(df)

if __name__ == "__main__":
    fetcher = LinksFetcher()
    fetcher.run()
