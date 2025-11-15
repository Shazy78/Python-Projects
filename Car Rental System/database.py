import psycopg2
from psycopg2 import sql
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            print("✅ Connected to PostgreSQL database successfully!")
        except Exception as e:
            print(f"❌ Error connecting to database: {e}")

    def execute_query(self, query, params=None, fetch=False):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                if query.strip().upper().startswith('SELECT'):
                    result = cursor.fetchall()
                    cursor.close()
                    return result
                else:
                    self.connection.commit()
                    cursor.close()
                    return True
            else:
                self.connection.commit()
                cursor.close()
                return True
        except Exception as e:
            print(f"❌ Database error: {e}")
            return False

    def fetch_all(self, query, params=None):
        return self.execute_query(query, params, fetch=True)

    def fetch_one(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as e:
            print(f"❌ Database error: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()
            print("✅ Database connection closed.")