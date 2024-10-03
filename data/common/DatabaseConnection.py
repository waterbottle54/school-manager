import sqlite3


class DatabaseConnection:

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection: sqlite3.Connection | None = None

    def __enter__(self):
        # Establish the connection
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the connection
        if self.connection:
            self.connection.close()
