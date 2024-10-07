from time import time
from data.common.DataObject import *


class Student(DataObject["Student"]):

    def __init__(self, name: str, grade: int, school: str, id=-1, created=-1):
        super().__init__()
        self.id = id
        self.name = name
        self.grade = grade
        self.school = school
        self.created = created if created != -1 else int(time())

    def to_record(self) -> dict[str, object]:
        return {
            "s_id": self.id,
            "name": self.name,
            "grade": self.grade,
            "school": self.school,
            "created": self.created,
        }

    @staticmethod
    def from_record(record: list[object]) -> "Student":
        id = DataObject.cast(record[0], int)
        name = DataObject.cast(record[1], str)
        grade = DataObject.cast(record[2], int)
        school = DataObject.cast(record[3], str)
        created = DataObject.cast(record[4], int)
        return Student(name, grade, school, id, created)
