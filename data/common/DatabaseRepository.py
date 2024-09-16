from data.common.DatabaseConnection import *
from abc import ABC, abstractmethod

class DatabaseRepository:

    db_name: str
    table_name: str
    pk_name: str

    def __init__(self, db_name, table_name, pk_name):
        self.db_name = db_name
        self.table_name = table_name
        self.pk_name = pk_name
        with DatabaseConnection(db_name) as db:
            db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            result = db.cursor.fetchone()
            if result is None:
                self.on_create_table(db)

    @abstractmethod
    def on_create_table(self, db: DatabaseConnection):
        pass

    @abstractmethod
    def to_object(self, row):
        pass
    
    def query(self, sql) -> list:
        list = []
        with DatabaseConnection(self.db_name) as db:
            db.cursor.execute(sql)
            db.connection.commit()
            rows = db.cursor.fetchall()
            for row in rows:
                objects = self.to_object(row)
                list.append(objects)
        return list
    
    def insert(self, data: dict, auto_key: bool):
        if auto_key:
            del data[self.pk_name]
        sql = f'INSERT INTO {self.table_name} '
        sql += self.to_tuple_format(data.keys(), False)
        sql += ' VALUES '
        sql += self.to_tuple_format(data.values(), True)
        with DatabaseConnection(self.db_name) as db:
            db.cursor.execute(sql)
            db.connection.commit()

    def delete(self, id):
        with DatabaseConnection(self.db_name) as db:
            db.cursor.execute(f"DELETE FROM {self.table_name} WHERE {self.pk_name} == '{id}'")
            db.connection.commit()

    def to_tuple_format(self, values, quotation: bool):
        sql = '('
        for i, value in enumerate(values):
            if i != 0:
                sql += ', '
            if isinstance(value, str):
                if quotation is True:
                    sql += f"'{value}'"
                else:
                    sql += value
            else:
                sql += str(value)
        sql += ')'
        return sql