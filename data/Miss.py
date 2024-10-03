from time import time

from data.common.DataObject import *
from data.ProblemHeader import ProblemHeader


class Miss(DataObject["Miss"]):

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

    def to_record(self) -> dict[str, object]:
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

    @staticmethod
    def from_record(record: list[object]) -> "Miss":

        if len(record) != 10:
            raise Exception(
                "Cannot convert DB record into Miss instance: Count of record columns != 10"
            )

        id = DataObject.cast(record[0], int)
        student_id = DataObject.cast(record[1], int)
        problem_id = DataObject.cast(record[2], int)
        grade = DataObject.cast(record[3], int)
        chapter = DataObject.cast(record[4], str)
        book = DataObject.cast(record[5], str)
        title = DataObject.cast(record[6], str)
        _record = DataObject.cast(record[7], str)
        updated = DataObject.cast(record[8], int)
        created = DataObject.cast(record[9], int)

        problem_header = ProblemHeader(grade, chapter, book, title)
        return Miss(
            student_id, problem_id, problem_header, _record, id, updated, created
        )
