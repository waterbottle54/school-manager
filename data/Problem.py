from time import *
import json

class Problem:

    id: int
    grade: int
    chapter: str
    book: str
    num_choice: int
    ans_mcq: list       # answers for a multicle choice question
    ans_saq: dict       # answers for a short-answer question (key is description for subquestions)
    created: int

    def __init__(self, grade: int, chapter: str, book: str, num_choice: int, 
                 ans_msq: list, ans_saq: dict, id=-1, created=int(time())):
        self.id = id
        self.grade = grade
        self.chapter = chapter
        self.book = book
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
            'num_choice': self.num_choice,
            'ans_mcq': json.dump(self.ans_mcq),
            'ans_saq': json.dump(self.ans_saq),
            'created': self.created
        }
    
    def from_record(id: int, grade: int, chapter: str, book: str, 
                    num_choice: int, json_ans_mcq: str, json_ans_saq: str, created: int):
        problem = Problem(0,'','',0,[],{})
        problem.id = id
        problem.grade = grade
        problem.chapter = chapter
        problem.book = book
        problem.num_choice = num_choice
        problem.ans_mcq = json.load(json_ans_mcq)
        problem.ans_saq = json.load(json_ans_saq)
        problem.created = created

        for key, answer in problem.ans_saq.items():
            answer: str
            answer = answer.replace('#comma#', ',').replace('#colon#', ':')
            problem.ans_saq[key] = answer

        return problem