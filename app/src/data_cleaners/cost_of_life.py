import pandas as pd
import re

def clean_cost_of_life(df):
    """
    Nettoie les données du coût de la vie.
    - Supprime les lignes avec des valeurs manquantes (sauf description).
    - Convertit les valeurs numériques correctement.
    - Remplace les descriptions manquantes par 'unknown'.
    """
    df = df.drop_duplicates()

    # Extraction des valeurs et des unités monétaires
    def extract_value_and_currency(value):
        match = re.search(r"(\d+(\.\d+)?)\s*(\w+)", str(value))
        if match:
            numeric_value = float(match.group(1))
            currency = match.group(3)
            return numeric_value, currency
        return None, None

    df[["value", "unitValue"]] = df["value"].apply(lambda p: pd.Series(extract_value_and_currency(p)))

    # Nettoyage du champ 'description'
    df["description"] = df.get("description", "").astype(str).str.strip()
    df["description"] = df["description"].replace("", "unknown")
    df["description"] = df["description"].fillna("unknown")

    # Supprime les lignes où 'price' est NaN (valeur numérique non reconnue)
    df = df.dropna(subset=["value"])

    # Renommage final
    df.rename(columns={"value": "price", "unitValue": "unitprice"}, inplace=True)
    return df[["country", "description", "price", "unitprice"]]
