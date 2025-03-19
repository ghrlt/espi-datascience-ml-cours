import pandas as pd
import json
from db.repository import Repository

def normalize_columns(matrix):
    """
    Normalise les colonnes numériques du DataFrame.
    Utilise la normalisation Min-Max (0-1) tout en évitant les divisions par zéro et NaN.
    """
    numeric_columns = matrix.select_dtypes(include=['number']).columns

    for col in numeric_columns:
        min_value = matrix[col].min()
        max_value = matrix[col].max()

        if pd.isna(min_value) or pd.isna(max_value):  
            print(f"⚠️ Colonne {col} contient uniquement des NaN, mise à zéro.")
            matrix[col] = 0  # Remplace par 0
        elif max_value > min_value:
            matrix[col] = (matrix[col] - min_value) / (max_value - min_value)  # Normalisation min-max
        else:
            print(f"⚠️ Colonne {col} a un seul type de valeur ({min_value}), mise à 0.")
            matrix[col] = 0

    return matrix

def get_matrix():
    repo = Repository()

    # Récupérer les données nécessaires
    data = repo.fetch_all("clean_data_cost_of_life")
    data_crime_index = repo.fetch_all("clean_data_crime")

    # Transformer en DataFrame
    df = pd.DataFrame(data, columns=['id', 'country', 'description', 'price', 'unitPrice'])
    df_crime_index = pd.DataFrame(data_crime_index, columns=['id', 'country', 'description', 'value', 'unit'])

    # Charger le mapping des colonnes
    with open("app/src/matrix/mapped_column.json", "r") as f:
        column_mapping = json.load(f)

    column_mapping = {key.strip().lower(): value for key, value in column_mapping.items()}

    # Nettoyage des descriptions
    df["description"] = df["description"].str.strip().str.lower()

    # Mapper les descriptions en colonnes
    df["column_name"] = df["description"].map(column_mapping)

    # Supprimer les valeurs non mappées
    df = df.dropna(subset=["column_name"])

    # Supprimer les doublons en prenant la moyenne des valeurs
    df = df.groupby(["country", "column_name"], as_index=False)["price"].mean()

    # Pivot pour obtenir une matrice pays x indicateurs
    matrix = df.pivot(index="country", columns="column_name", values="price").reset_index()

    # Ajouter le crime index
    df_crime_index = df_crime_index.groupby("country", as_index=False)["value"].mean()
    df_crime_index.rename(columns={"value": "crime_index"}, inplace=True)

    matrix = matrix.merge(df_crime_index[['country', 'crime_index']], on='country', how='left')

    # Remplacement des NaN par 0
    matrix = matrix.fillna(0)

    # Appliquer la normalisation
    matrix = normalize_columns(matrix)

    # Enregistrer dans la base de données
    repo.insert_data("matrix_cost_of_life", matrix)
    repo.close()

    print("✅ Matrice générée et insérée avec succès.")

if __name__ == "__main__":
    get_matrix()
