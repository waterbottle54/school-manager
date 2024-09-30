from PyQt5.QtCore import QObject, pyqtSignal

from common.LiveData import *
from data.common.ListDictRepository import *
from data.common.ListRepository import *
from data.ProblemHeader import *
from data.ProblemRepository import *
from data.Student import *
from data.StudentRepository import *


class StudentViewModel(QObject):

    class Event:
        pass

    class PromptStudent(Event):
        pass

    class ConfirmDeleteStudent(Event):
        student: Student

        def __init__(self, student: Student):
            self.student = student

    class NavigateToMissScreen(Event):
        student: Student

        def __init__(self, student):
            self.student = student

    event: pyqtSignal = pyqtSignal(Event)

    student_index: MutableLiveData
    can_delete_student: LiveData

    student_list: MutableLiveData
    current_student: LiveData
    student_repository: StudentRepository
    problem_repository: ProblemRepository

    def __init__(self):
        super().__init__()

        self.student_repository = StudentRepository()
        self.problem_repository = ProblemRepository()

        self.student_list = MutableLiveData([])
        self.student_index = MutableLiveData(-1)

        self.current_student = map2(
            self.student_list,
            self.student_index,
            lambda list, i: list[i] if i >= 0 and i < len(list) else None,
        )

        self.can_delete_student = map(
            self.current_student, lambda student: student is not None
        )

    def on_start(self):
        self.update_student_list()
        self.student_index.set_value(0)

    def on_add_problem_result(self, problem: Problem):
        print(str(problem.to_record()))

    def on_student_click(self, row, column):
        self.student_index.set_value(row)

    def on_add_student_click(self):
        self.event.emit(StudentViewModel.PromptStudent())

    def on_add_student_result(self, student: Student):
        self.student_repository.insert(student)
        self.update_student_list()

    def on_delete_student_click(self):
        student = self.current_student.value
        if student is not None:
            self.event.emit(StudentViewModel.ConfirmDeleteStudent(student))

    def on_delete_student_confirm(self, student: Student):
        self.student_repository.delete(student.id)
        self.update_student_list()

    def on_miss_manage_click(self):
        student = self.current_student.value
        if student is not None:
            self.event.emit(StudentViewModel.NavigateToMissScreen(student))

    def update_student_list(self):
        list = self.student_repository.query()
        self.student_list.set_value(list if list is not None else [])
