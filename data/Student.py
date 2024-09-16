from time import *

class Student:
    id: int
    name: str
    grade: int
    school: str
    created: int

    def __init__(self, name, grade, school, id=-1, created=int(time())):
        super().__init__()
        self.id = id
        self.name = name
        self.grade = grade
        self.school = school
        self.created = created

    def to_record(self):
        return {
            's_id': self.id,
            'name': self.name,
            'grade': self.grade,
            'school': self.school,
            'created': self.created
        }