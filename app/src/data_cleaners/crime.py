import pandas as pd

def clean_crime(df):
    """
    Nettoie les données de criminalité.
    - Garde les descriptions, remplace les manquantes par 'unknown'.
    - Supprime les valeurs non numériques.
    """
    df = df.drop_duplicates()

    df["description"] = df.get("description", "").astype(str).str.strip()
    df["description"] = df["description"].replace("", "unknown")
    df["description"] = df["description"].fillna("unknown")

    df = df[pd.to_numeric(df["value"], errors="coerce").notna()]
    df["value"] = df["value"].astype(float)

    return df[["country", "description", "value", "unit"]]
