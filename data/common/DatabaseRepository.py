from abc import abstractmethod

from data.common.LiveData import LiveData, MutableLiveData
from data.common.DatabaseConnection import *
from abc import ABC


class DatabaseRepository[T](ABC):

    def __init__(self, db_name: str, table_name: str, pk_name: str, version: int):

        self._db_name = db_name
        self._table_name = table_name
        self._pk_name = pk_name
        self._version = version
        self._livedata_by_query = dict[str, MutableLiveData[list[T]]]({})

        with DatabaseConnection(db_name) as db:
            # version migration if needed
            original_version = self.get_db_version(db)
            if original_version != version:
                self.set_db_version(db, self._version)
                db.cursor.execute(f"DROP TABLE IF EXISTS {self._table_name}")
                if db.connection is not None:
                    db.connection.commit()

            # table creation
            db.cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,),
            )
            result = db.cursor.fetchone()
            if result is None:
                self.on_create_table(db)

    @abstractmethod
    def on_create_table(self, db: DatabaseConnection):
        pass

    @abstractmethod
    def to_object(self, record: list[object]) -> T:
        pass

    # db info accessors

    def get_db_version(self, db: DatabaseConnection) -> int:
        db.cursor.execute("CREATE TABLE IF NOT EXISTS version_info (version INTEGER)")
        db.cursor.execute("SELECT version FROM version_info")
        result = db.cursor.fetchone()
        return result[0] if result else -1

    def set_db_version(self, db: DatabaseConnection, version):
        db.cursor.execute(
            "INSERT OR REPLACE INTO version_info (rowid, version) VALUES (1, ?)",
            (version,),
        )
        if db.connection is not None:
            db.connection.commit()

    # DML operations

    def query(self, sql: str, args: tuple = tuple()) -> list[T]:
        result_list = list[T]()
        with DatabaseConnection(self._db_name) as db:
            db.cursor.execute(sql, args)
            if db.connection is not None:
                db.connection.commit()
            records: list[list[object]] = db.cursor.fetchall()
            for record in records:
                _object = self.to_object(record)
                result_list.append(_object)
        return result_list

    def get_livedata(self, sql_query: str) -> LiveData[list[T]]:
        if sql_query in self._livedata_by_query:
            return self._livedata_by_query[sql_query]
        else:
            _list = self.query(sql_query)
            self._livedata_by_query[sql_query] = MutableLiveData(_list)
            return self._livedata_by_query[sql_query]

    def _reload_livedata(self):
        for sql_query, livedata in self._livedata_by_query.items():
            livedata.set_value(self.query(sql_query))

    def insert(self, data: dict[str, object], need_generate_key: bool):
        if need_generate_key:
            del data[self._pk_name]

        columns = ", ".join(data.keys())
        values = ", ".join([self.format_value(value) for value in data.values()])

        with DatabaseConnection(self._db_name) as db:
            db.cursor.execute(
                f"INSERT INTO {self._table_name} ({columns}) VALUES ({values})"
            )
            if db.connection is not None:
                db.connection.commit()
                self._reload_livedata()

    def update(self, data: dict[str, object]):
        id = data.pop(self._pk_name)
        columns = ", ".join([f"{key} = ?" for key in data.keys()])
        with DatabaseConnection(self._db_name) as db:
            db.cursor.execute(
                f"UPDATE {self._table_name} SET {columns} WHERE {self._pk_name} = ?",
                (
                    *data.values(),
                    id,
                ),
            )
            if db.connection is not None:
                db.connection.commit()
                self._reload_livedata()

    def delete(self, id: int | str):
        with DatabaseConnection(self._db_name) as db:
            db.cursor.execute(
                f"DELETE FROM {self._table_name} WHERE {self._pk_name} = ?", (id,)
            )
            if db.connection is not None:
                db.connection.commit()
                self._reload_livedata()

    def format_value(self, value: object) -> str:
        if isinstance(value, str):
            return f"'{value}'"
        return str(value)
