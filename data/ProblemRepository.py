from data.common.DatabaseConnection import *
from data.common.DatabaseRepository import *
from data.Problem import *

class ProblemRepository(DatabaseRepository):

    def __init__(self):
            super().__init__('db_app', 'problem', 'p_id')

    def on_create_table(self, db):
        db.cursor.execute(f'''
            CREATE TABLE {self.table_name} (
            p_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            grade INTEGER NOT NULL,
            chapter TEXT NOT NULL,
            book TEXT NOT NULL,
            num_choice INTEGER NOT NULL,
            ans_mcq TEXT NOT NULL,
            ans_saq TEXT NOT NULL,
            created INTEGER                 
        )''')

    def to_object(self, row):
        id = row[0]
        title = row[1]
        grade = row[2]
        chapter = row[3]
        book = row[4]
        num_choice = row[5]
        ans_mcq = row[6]
        ans_saq = row[7]
        created = row[8]
        return Problem.from_record(id, title, grade, chapter, book, num_choice, ans_mcq, ans_saq, created)
    
    def query(self) -> list:
        return super().query(f'SELECT * FROM {self.table_name} ORDER BY created DESC')
    
    def insert(self, problem: Problem):
        super().insert(problem.to_record(), problem.id == -1)

    def delete(self, id: int):
        super().delete(id)