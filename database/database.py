import sqlite3
from pathlib import Path

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            db_path = Path(__file__).parent / "finance.db"
            cls._instance.connection = sqlite3.connect(db_path)
            cls._instance.connection.row_factory = sqlite3.Row
            cls._instance.cursor = cls._instance.connection.cursor()
        return cls._instance

    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.connection.commit()

    def executemany(self, query, params):
        self.cursor.executemany(query, params)
        self.connection.commit()

    def fetchone(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetchall(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

db = Database()