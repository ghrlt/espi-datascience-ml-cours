import pandas as pd

def clean_healthcare(df):
    """
    Nettoie les données de soins de santé.
    - Description : remplacement des vides par 'unknown'.
    - Conversion des valeurs en float.
    """
    df = df.drop_duplicates()

    df["description"] = df.get("description", "").astype(str).str.strip()
    df["description"] = df["description"].replace("", "unknown")
    df["description"] = df["description"].fillna("unknown")

    df = df[pd.to_numeric(df["value"], errors="coerce").notna()]
    df["value"] = df["value"].astype(float)

    return df[["country", "description", "value", "unit"]]
