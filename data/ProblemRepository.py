from data.common.DatabaseConnection import *
from data.common.DatabaseRepository import *
from data.Problem import *
from data.ProblemHeader import *


class ProblemRepository(DatabaseRepository["Problem"]):

    _instance: "ProblemRepository | None" = None

    @staticmethod
    def get_instance() -> "ProblemRepository":
        if ProblemRepository._instance is None:
            ProblemRepository._instance = ProblemRepository()
        return ProblemRepository._instance

    def __init__(self):
        super().__init__("db_app", "problem", "p_id", 1)

    def on_create_table(self, db):
        db.cursor.execute(
            f"""
            CREATE TABLE {self._table_name} (
            p_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            grade INTEGER NOT NULL, 
            chapter TEXT NOT NULL, 
            book TEXT NOT NULL, 
            title TEXT NOT NULL, 
            num_choice INTEGER NOT NULL, 
            ans_mcq TEXT NOT NULL, 
            ans_saq TEXT NOT NULL, 
            created INTEGER
            )
            """,
        )

    def to_object(self, record: list[object]) -> Problem:
        return Problem.from_record(record)

    def get_problems(self, book: str, grade: int, chapter: str) -> list[Problem]:
        ordering = """
            ORDER BY CASE 
            WHEN title NOT LIKE "%[^0-9]%" 
            THEN CAST(title AS INT) 
            ELSE 999999999 
            END ASC, title ASC
        """
        return super().query(
            f"""
            SELECT * FROM {self._table_name} 
            WHERE book = ? 
            AND grade = ? 
            AND chapter = ? 
            {ordering}
            """,
            (book, grade, chapter),
        )

    def get_problem_by_header(self, h: ProblemHeader) -> Problem | None:
        _list = super().query(
            f"""
            SELECT * FROM {self._table_name} 
            WHERE book = ? 
            AND grade = ? 
            AND chapter = ? 
            AND title = ?
            """,
            (h.book, h.grade, h.chapter, h.title),
        )
        return _list[0] if (len(_list) > 0) else None

    def insert(self, problem: Problem):
        super().insert(problem.to_record(), problem.id == -1)

    def update(self, problem: Problem):
        super().update(problem.to_record())

    def delete(self, id: int):
        super().delete(id)
