import pandas as pd

def clean_cost_of_life(df):
    """
    Nettoie les données du coût de la vie.
    - Supprime les lignes avec des valeurs manquantes.
    - Convertit les valeurs numériques correctement.
    """
    df = df.dropna()
    df = df.drop_duplicates()

    # Extraction des valeurs et des unités monétaires
    def extract_value_and_currency(value):
        import re
        match = re.search(r"(\d+(\.\d+)?)\s*(\w+)", value)
        if match:
            numeric_value = float(match.group(1))
            currency = match.group(3)
            return numeric_value, currency
        return None, None

    df[['value', 'unitValue']] = df['value'].apply(
        lambda p: pd.Series(extract_value_and_currency(str(p)))
    )

    # 🚀 Fix: Rename `value` -> `price`, `unitValue` -> `unitprice` before returning
    df.rename(columns={"value": "price", "unitValue": "unitprice"}, inplace=True)

    return df
