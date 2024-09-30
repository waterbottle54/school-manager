from abc import abstractmethod

from data.common.DatabaseConnection import *


class DatabaseRepository:

    db_name: str
    table_name: str
    pk_name: str
    version: int

    def __init__(self, db_name, table_name, pk_name, version):

        self.db_name = db_name
        self.table_name = table_name
        self.pk_name = pk_name
        self.version = version

        with DatabaseConnection(db_name) as db:
            # version migration if needed
            original_version = self.get_db_version(db)
            if original_version != version:
                self.set_db_version(db, self.version)
                db.cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")
                db.connection.commit()

            # table creation
            db.cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,),
            )
            result = db.cursor.fetchone()
            if result is None:
                self.on_create_table(db)

    def get_db_version(self, db: DatabaseConnection):
        db.cursor.execute("CREATE TABLE IF NOT EXISTS version_info (version INTEGER)")
        db.cursor.execute("SELECT version FROM version_info")
        result = db.cursor.fetchone()
        return result[0] if result else -1

    def set_db_version(self, db: DatabaseConnection, version):
        db.cursor.execute(
            "INSERT OR REPLACE INTO version_info (rowid, version) VALUES (1, ?)",
            (version,),
        )
        db.connection.commit()

    @abstractmethod
    def on_create_table(self, db: DatabaseConnection):
        pass

    @abstractmethod
    def to_object(self, row):
        pass

    def query(self, sql, args=tuple()) -> list:
        list = []
        with DatabaseConnection(self.db_name) as db:
            db.cursor.execute(sql, args)
            db.connection.commit()
            rows = db.cursor.fetchall()
            for row in rows:
                objects = self.to_object(row)
                list.append(objects)
        return list

    def insert(self, data: dict, auto_key: bool):
        if auto_key:
            del data[self.pk_name]

        columns = ", ".join(data.keys())
        values = ", ".join([self.format_value(value) for value in data.values()])

        with DatabaseConnection(self.db_name) as db:
            db.cursor.execute(
                f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})"
            )
            db.connection.commit()

    def update(self, data: dict):
        id = data.pop(self.pk_name)
        columns = ", ".join([f"{key} = ?" for key in data.keys()])
        with DatabaseConnection(self.db_name) as db:
            db.cursor.execute(
                f"UPDATE {self.table_name} SET {columns} WHERE {self.pk_name} = ?",
                (
                    data.values(),
                    id,
                ),
            )
            db.connection.commit()

    def delete(self, id):
        with DatabaseConnection(self.db_name) as db:
            db.cursor.execute(
                f"DELETE FROM {self.table_name} WHERE ? == ?", (self.pk_name, id)
            )
            db.connection.commit()

    def format_value(self, value):
        if isinstance(value, str):
            return f"'{value}'"
        return str(value)