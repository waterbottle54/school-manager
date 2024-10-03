from data.Problem import *


class ProblemHeader:

    def __init__(self, grade: int, chapter: str, book: str, title: str):
        self.grade = grade
        self.chapter = chapter
        self.book = book
        self.title = title

    def matches(self, problem: Problem) -> bool:
        return (
            self.grade == problem.grade
            and self.chapter == problem.chapter
            and self.book == problem.book
            and self.title == problem.title
        )

    @staticmethod
    def from_problem(problem: Problem):
        return ProblemHeader(
            problem.grade, problem.chapter, problem.book, problem.title
        )
