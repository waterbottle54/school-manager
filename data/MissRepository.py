from data.common.DatabaseConnection import DatabaseConnection
from data.common.DatabaseRepository import *
from data.Miss import *


class MissRepository(DatabaseRepository):

    def __init__(self):
        super().__init__("db_app", "miss", "m_id", 1)

    def on_create_table(self, db: DatabaseConnection):
        db.cursor.execute(
            f"""
            CREATE TABLE {self.table_name} (
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

    def to_object(self, row):
        id = row[0]
        student_id = row[1]
        problem_id = row[2]
        grade = row[3]
        chapter = row[4]
        book = row[5]
        title = row[6]
        record = row[7]
        updated = row[8]
        created = row[9]
        return Miss.from_record(
            id,
            student_id,
            problem_id,
            grade,
            chapter,
            book,
            title,
            record,
            updated,
            created,
        )

    def query(self, m_id: int) -> list:
        return super().query(f"SELECT * FROM {self.table_name} WHERE m_id = ?", (m_id,))

    def query_by_student_id(self, student_id) -> list:
        return super().query(
            f"SELECT * FROM {self.table_name} WHERE student_id = ? ORDER BY updated DESC",
            (student_id,),
        )

    def insert(self, miss: Miss):
        super().insert(miss.to_record(), miss.id == -1)

    def update(self, miss: Miss):
        super().update(miss.to_record())

    def delete(self, id: int):
        super().delete(id)
