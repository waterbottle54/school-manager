from time import time

from data.ProblemHeader import ProblemHeader


class Miss:

    id: int
    student_id: int
    problem_id: int
    problem_header: ProblemHeader
    record: str
    updated: int
    created: int

    def __init__(
        self,
        student_id: int,
        problem_id: int,
        problem_header: ProblemHeader,
        record="",
        id=-1,
        updated=0,
        created=0,
    ):
        self.id = id
        self.student_id = student_id
        self.problem_id = problem_id
        self.problem_header = problem_header
        self.record = record
        self.updated = updated if updated != 0 else int(time())
        self.created = created if created != 0 else int(time())

    def to_record(self):
        return {
            "m_id": self.id,
            "student_id": self.student_id,
            "problem_id": self.problem_id,
            "grade": self.problem_header.grade,
            "chapter": self.problem_header.chapter,
            "book": self.problem_header.book,
            "title": self.problem_header.title,
            "record": self.record,
            "updated": self.updated,
            "created": self.created,
        }

    def from_record(
        id: int,
        student_id: int,
        problem_id: int,
        grade: int,
        chapter: str,
        book: str,
        title: str,
        record: str,
        updated: int,
        created: int,
    ):
        problem_header = ProblemHeader(grade, chapter, book, title)
        return Miss(
            student_id, problem_id, problem_header, record, id, updated, created
        )
