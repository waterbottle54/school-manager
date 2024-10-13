from data.common.DatabaseConnection import *
from data.common.DatabaseRepository import *
from data.Student import *


class StudentRepository(DatabaseRepository["Student"]):

    _instance: "StudentRepository | None" = None

    @staticmethod
    def get_instance() -> "StudentRepository":
        if StudentRepository._instance is None:
            StudentRepository._instance = StudentRepository()
        return StudentRepository._instance

    def __init__(self):
        super().__init__("db_app", "student", "s_id", 1)

    def on_create_table(self, db):
        db.cursor.execute(
            f"""
            CREATE TABLE {self._table_name} (
            s_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL, 
            grade INTEGER NOT NULL, 
            school TEXT NOT NULL, 
            created INTEGER
            )
            """
        )

    def to_object(self, row):
        id = row[0]
        name = row[1]
        grade = row[2]
        school = row[3]
        created = row[4]
        return Student(name, grade, school, id, created)

    def _sql_query_all(self) -> str:
        return f"SELECT * FROM {self._table_name} ORDER BY grade DESC"

    def get_students(self) -> list[Student]:
        return super().query(self._sql_query_all())

    def get_students_live(self) -> LiveData[list[Student]]:
        return super().get_livedata(self._sql_query_all())

    def insert(self, student: Student):
        super().insert(student.to_record(), student.id == -1)

    def delete(self, id: int):
        super().delete(id)
