from data.Miss import Miss
from data.common.DatabaseConnection import DatabaseConnection
from data.common.DatabaseRepository import *
from data.Miss import *


class MissRepository(DatabaseRepository[Miss]):

    _instance: "MissRepository | None" = None

    @staticmethod
    def get_instance() -> "MissRepository":
        if MissRepository._instance is None:
            MissRepository._instance = MissRepository()
        return MissRepository._instance

    def __init__(self):
        super().__init__("db_app", "miss", "m_id", 1)

    def on_create_table(self, db: DatabaseConnection):
        db.cursor.execute(
            f"""
            CREATE TABLE {self._table_name} (
            m_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            student_id INTEGER NOT NULL, 
            problem_id INTEGER NOT NULL, 
            grade INTEGER NOT NULL, 
            chapter TEXT NOT NULL, 
            book TEXT NOT NULL, 
            title TEXT NOT NULL, 
            record TEXT NOT NULL, 
            updated INTEGER, 
            created INTEGER
            )
            """
        )

    def to_object(self, record: list[object]) -> Miss:
        return Miss.from_record(record)

    def get_miss_by_id(self, m_id: int) -> Miss | None:
        _list = super().query(
            f"SELECT * FROM {self._table_name} WHERE m_id = ?", (m_id,)
        )
        return _list[0] if len(_list) > 0 else None

    def get_misses_by_student_id(self, student_id) -> list[Miss]:
        return super().query(
            f"SELECT * FROM {self._table_name} WHERE student_id = ? ORDER BY updated DESC",
            (student_id,),
        )

    def insert(self, miss: Miss):
        super().insert(miss.to_record(), miss.id == -1)

    def update(self, miss: Miss):
        super().update(miss.to_record())

    def delete(self, id: int):
        super().delete(id)
