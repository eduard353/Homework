import sqlite3
import os


class DataConn:

    def __init__(self, db_name='rss_cache.db'):
        """Конструктор"""
        self.db_name = db_name

    def __enter__(self):
        """
        Открываем подключение с базой данных.
        """
        db_exists = os.path.exists(self.db_name)
        self.conn = sqlite3.connect(self.db_name)
        if not db_exists:
            with open('db_schema.sql', 'r') as f:
                schema = f.read()
                self.conn.executescript(schema)

        else:
            print('DB exists.')
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Закрываем подключение.
        """
        self.conn.close()
        if exc_val:
            raise

