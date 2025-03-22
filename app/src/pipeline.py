from db.repository import Repository
from db.init import initialize_database
import pandas as pd
from data_fetchers.cost_of_life import CostOfLifeScraper
from data_fetchers.crime import CrimeScraper
from data_fetchers.healthcare import HealthCareScraper
from data_fetchers.pollution import PollutionScraper
from data_fetchers.quality_of_life import QualityOfLifeScraper

from data_fetchers.links_fetcher import LinksFetcher

from data_cleaners.cost_of_life import clean_cost_of_life
from data_cleaners.crime import clean_crime
from data_cleaners.healthcare import clean_healthcare
from data_cleaners.pollution import clean_pollution
from data_cleaners.quality_of_life import clean_quality_of_life

from matrix.get import get_matrix

def run_pipeline(count: int = 0):
    """
    Pipeline complet pour récupérer, nettoyer et stocker les données dans la base PostgreSQL.
    """

    if count == 0:
        print("🔄 Début du pipeline...", flush=True)
    elif count == 1:
        print("🔄 Redémarrage du pipeline...", flush=True)
    elif count == 2:
        print("🔄 Deuxième redémarrage du pipeline...", flush=True)
    else:
        print("❌ Bouclage potentiellement infini détecté, arrêt du pipeline.", flush=True)
        return

    repo = Repository()
    if repo.should_init:
        print("⚠️ Base de données non initialisée, initialisation...")
        initialize_database()
        return run_pipeline(count+1)

    urls = repo.fetch_all("links")
    if not urls:
        print("❌ Aucun lien trouvé dans la base de données.")
        LinksFetcher().run()
        return run_pipeline(count+1)

    print("🔗 Liens récupérés avec succès !"
          f"\n🔗 {len(urls)} liens trouvés.")
    
    # # Limiter à quelques pays pour test et avoid le ban 429
    # selected_countries = ["France", "Germany", "Japan"]
    # urls = [url for url in urls if url[1] in selected_countries]

    print("🌍 Pays sélectionnés pour le scraping :", [u[1] for u in urls])



    scrapers = {
        "cost-of-living": (CostOfLifeScraper, clean_cost_of_life, "clean_data_cost_of_life"),
        "crime": (CrimeScraper, clean_crime, "clean_data_crime"),
        # "health-care": (HealthCareScraper, clean_healthcare, "clean_data_health_care"),
        # "pollution": (PollutionScraper, clean_pollution, "clean_data_pollution"),
        # "quality-of-life": (QualityOfLifeScraper, clean_quality_of_life, "clean_data_quality_of_life")
    }

    for name, (ScraperClass, cleaner, table) in scrapers.items():
        print(f"🚀 Fetching {name} data...", flush=True)
        scraper = ScraperClass(f"https://www.numbeo.com/{name}/")
        
        combined_data = []
        for row in urls:
            country = row[1]
            url = row[2]
            raw_df = scraper.get_data([url])
            if not raw_df.empty:
                raw_df["country"] = country
                combined_data.append(raw_df)

        if not combined_data:
            print(f"⚠️ No data fetched for {name}, skipping...")
            continue

        full_df = pd.concat(combined_data, ignore_index=True)
        clean_data = cleaner(full_df)
        print(clean_data.head(), flush=True)


        if clean_data.empty:
            print(f"⚠️ No clean data available for {name}, skipping...")
            continue

        repo.insert_data(table, clean_data)

    repo.close()

    # Ajouter la génération de matrice
    print("🧠 Génération de la matrice normalisée...", flush=True)
    get_matrix()

    print("✅ Pipeline terminé avec succès !", flush=True)


if __name__ == "__main__":
    run_pipeline()
