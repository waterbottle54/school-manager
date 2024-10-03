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
