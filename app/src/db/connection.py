import psycopg2

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="postgres",
            dbname="cours_data",
            user="root",
            password="root",
            port=5432
        )
        self.cursor = self.conn.cursor()

    def table_exists(self, table_name):
        sql = f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}')"
        return self.query(sql)[0][0]

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchall()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
