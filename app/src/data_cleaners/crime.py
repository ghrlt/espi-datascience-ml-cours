import pandas as pd

def clean_crime(df):
    """
    Nettoie les données de criminalité.
    - Supprime les valeurs manquantes.
    - Convertit les valeurs en float.
    """
    df = df.dropna()
    df = df.drop_duplicates()
    
    df = df[pd.to_numeric(df['value'], errors='coerce').notna()]
    df['value'] = df['value'].astype(float)

    return df
