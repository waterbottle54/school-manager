from time import *
import json

class Problem:

    id: int
    grade: int
    chapter: str
    book: str
    title: str
    num_choice: int
    ans_mcq: list       # answers for a multicle choice question
    ans_saq: dict       # answers for a short-answer question (key is description for subquestions)
    created: int

    def __init__(self, grade: int, chapter: str, book: str, title: str, 
                 num_choice: int, ans_msq: list, ans_saq: dict, id=-1, created=int(time())):
        self.id = id
        self.grade = grade
        self.chapter = chapter
        self.book = book
        self.title = title
        self.num_choice = num_choice
        self.ans_mcq = ans_msq
        self.ans_saq = ans_saq
        self.created = created

    def to_record(self):
        for key, answer in self.ans_saq.items():
            answer: str
            answer = answer.replace(',', '#comma#').replace(':', '#colon#')
            self.ans_saq[key] = answer

        return {
            'p_id': self.id,
            'grade': self.grade,
            'chapter': self.chapter,
            'book': self.book,
            'title': self.title,
            'num_choice': self.num_choice,
            'ans_mcq': json.dumps(self.ans_mcq),
            'ans_saq': json.dumps(self.ans_saq),
            'created': self.created
        }
    
    def from_record(id: int, grade: int, chapter: str, book: str, title: str,
                    num_choice: int, json_ans_mcq: str, json_ans_saq: str, created: int):
        ans_mcq = json.loads(json_ans_mcq)
        ans_saq = json.loads(json_ans_saq)
        problem = Problem(grade, chapter, book, title, num_choice, ans_mcq, ans_saq, id, created)
        
        for key, answer in problem.ans_saq.items():
            answer: str
            answer = answer.replace('#comma#', ',').replace('#colon#', ':')
            problem.ans_saq[key] = answer

        return problem