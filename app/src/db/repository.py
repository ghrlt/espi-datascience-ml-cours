from db.connection import Database

class Repository:
    def __init__(self):
        self.db = Database()

    @property
    def should_init(self):
        # Vérifie si les tables sont déjà créées
        return not self.db.table_exists("links")

    def insert_data(self, table, df):
        if df.empty:
            print(f"⚠️ DataFrame vide, rien à insérer dans {table}")
            return

        cols = ", ".join(df.columns) # Nom des colonnes
        values_placeholder = ", ".join(["%s"] * len(df.columns)) # Placeholder pour les valeurs

        sql = f"INSERT INTO {table} ({cols}) VALUES ({values_placeholder}) ON CONFLICT DO NOTHING"
        
        try:
            for row in df.itertuples(index=False, name=None):
                self.db.execute(sql, row)
            print(f"✅ Données insérées dans {table} avec succès.")
        except Exception as e:
            print(f"❌ Erreur lors de l'insertion dans {table} : {e}")
            self.db.conn.rollback()

    def fetch_all(self, table):
        """
        Récupère toutes les données d'une table.
        :param table: Nom de la table
        :return: Liste des résultats
        """
        try:
            return self.db.query(f"SELECT * FROM {table}")
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des données de {table} : {e}")
            return []

    def fetch_one(self, table, condition_column, condition_value):
        """
        Récupère une ligne en fonction d'une condition.
        :param table: Nom de la table
        :param condition_column: Colonne sur laquelle appliquer la condition
        :param condition_value: Valeur à rechercher
        :return: Une ligne ou None
        """
        sql = f"SELECT * FROM {table} WHERE {condition_column} = %s LIMIT 1"
        try:
            result = self.db.query(sql, (condition_value,))
            return result[0] if result else None
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des données de {table} : {e}")
            return None

    def delete_all(self, table):
        """
        Supprime toutes les données d'une table.
        :param table: Nom de la table
        """
        try:
            self.db.execute(f"DELETE FROM {table}")
            print(f"🗑 Toutes les données de {table} ont été supprimées.")
        except Exception as e:
            print(f"❌ Erreur lors de la suppression des données de {table} : {e}")

    def close(self):
        """
        Ferme la connexion à la base de données.
        """
        self.db.close()
