import pandas as pd

def clean_quality_of_life(df):
    """
    Nettoie les données sur la qualité de vie.
    - Supprime les lignes avec des valeurs manquantes.
    - Convertit les valeurs en float.
    """
    df = df.dropna()
    df = df.drop_duplicates()

    df = df[pd.to_numeric(df['value'], errors='coerce').notna()]
    df['value'] = df['value'].astype(float)

    return df
