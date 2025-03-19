import pandas as pd

def clean_healthcare(df):
    """
    Nettoie les données de soins de santé.
    - Supprime les lignes avec des valeurs manquantes.
    - Convertit les valeurs en float.
    """
    df = df.dropna()
    df = df.drop_duplicates()

    df = df[pd.to_numeric(df['value'], errors='coerce').notna()]
    df['value'] = df['value'].astype(float)

    return df
