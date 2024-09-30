from data.common.DatabaseConnection import *
from data.common.DatabaseRepository import *
from data.Problem import *
from data.ProblemHeader import *


class ProblemRepository(DatabaseRepository):

    def __init__(self):
        super().__init__("db_app", "problem", "p_id", 1)

    def on_create_table(self, db):
        db.cursor.execute(
            f"""
            CREATE TABLE {self.table_name} (
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

    def to_object(self, row):
        id = row[0]
        grade = row[1]
        chapter = row[2]
        book = row[3]
        title = row[4]
        num_choice = row[5]
        ans_mcq = row[6]
        ans_saq = row[7]
        created = row[8]
        return Problem.from_record(
            id, grade, chapter, book, title, num_choice, ans_mcq, ans_saq, created
        )

    def query_all(self) -> list:
        return super().query(f"SELECT * FROM {self.table_name} ORDER BY created DESC")

    def query(self, book, grade, chapter) -> list:
        ordering = """
            ORDER BY CASE 
            WHEN title NOT LIKE "%[^0-9]%" 
            THEN CAST(title AS INT) 
            ELSE 999999999 
            END ASC, title ASC
        """
        return super().query(
            f"""
            SELECT * FROM {self.table_name} 
            WHERE book = ? 
            AND grade = ? 
            AND chapter = ? 
            {ordering}
            """,
            (book, grade, chapter),
        )

    def query_by_header(self, h: ProblemHeader) -> list:
        return super().query(
            f"""
            SELECT * FROM {self.table_name} 
            WHERE book = ? 
            AND grade = ? 
            AND chapter = ? 
            AND title = ?
            """,
            (h.book, h.grade, h.chapter, h.title),
        )

    def insert(self, problem: Problem):
        super().insert(problem.to_record(), problem.id == -1)

    def update(self, problem: Problem):
        super().update(problem.to_record())

    def delete(self, id: int):
        super().delete(id)
