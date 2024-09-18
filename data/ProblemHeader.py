from data.Problem import *

class ProblemHeader:
    grade: int
    chapter: str
    book: str
    title: str

    def __init__(self, grade: int, chapter: str, book: str, title: str):
        self.grade = grade
        self.chapter = chapter
        self.book = book
        self.title = title

    def matches(self, problem: Problem) -> bool:
        if problem is None:
            return False
        return self.grade == problem.grade and self.chapter == problem.chapter and self.book == problem.book and self.title == problem.title