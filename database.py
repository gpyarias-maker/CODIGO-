import psycopg2
from psycopg2.extras import RealDictCursor

class Database:

    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="personas",  
            user="postgres",
            password="123456",  # <-- Intenta con tu contraseña original aquí
            port=5432,
            client_encoding='utf8'
        )

    def execute(self, sql, params=None):
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sql, params or ())

        if sql.strip().lower().startswith("select"):
            result = cursor.fetchall()
        else:
            self.conn.commit()
            result = None

        cursor.close()
        return result

    def close(self):
        self.conn.close()