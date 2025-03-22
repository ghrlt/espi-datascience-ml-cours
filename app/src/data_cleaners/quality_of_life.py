import pandas as pd

def clean_quality_of_life(df):
    """
    Nettoie les données sur la qualité de vie.
    - Description fallback 'unknown'.
    - Valeurs numériques en float.
    """
    df = df.drop_duplicates()

    df["description"] = df.get("description", "").astype(str).str.strip()
    df["description"] = df["description"].replace("", "unknown")
    df["description"] = df["description"].fillna("unknown")

    df = df[pd.to_numeric(df["value"], errors="coerce").notna()]
    df["value"] = df["value"].astype(float)

    return df[["country", "description", "value", "unit"]]
