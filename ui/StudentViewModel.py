from PyQt5.QtCore import QObject, pyqtSignal

from data.common.LiveData import *
from data.common.DictOfListRepository import *
from data.common.ListRepository import *
from data.ProblemHeader import *
from data.ProblemRepository import *
from data.Student import *
from data.StudentRepository import *
from data.common.LiveList import LiveList


class StudentViewModel(QObject):

    class Event:
        pass

    class PromptStudent(Event):
        pass

    class ConfirmDeleteStudent(Event):
        def __init__(self, student: Student):
            self.student = student

    class NavigateToMissScreen(Event):
        def __init__(self, student):
            self.student = student

    event: pyqtSignal = pyqtSignal(Event)

    def __init__(self):
        super().__init__()

        self._student_repository = StudentRepository.get_instance()
        self._student_list = LiveList(self._student_repository.get_students_live())
        self.can_delete_student: LiveData[bool]

        self.can_delete_student = map(
            self._student_list.selected_livedata(),
            lambda selected: selected is not None,
        )

    def on_student_click(self, row: int, col: int):
        self._student_list.select_at(row)

    def on_add_student_click(self):
        self.event.emit(StudentViewModel.PromptStudent())

    def on_add_student_result(self, student: Student):
        self._student_list.set_default_index_on_update(True, lambda _, i_end, i: i_end)
        self._student_repository.insert(student)

    def on_delete_student_click(self):
        student_selected = self._student_list.selected_value()
        if student_selected is not None:
            self.event.emit(StudentViewModel.ConfirmDeleteStudent(student_selected))

    def on_delete_student_confirm(self, student: Student):
        self._student_repository.delete(student.id)

    def on_miss_manage_click(self):
        student_selected = self._student_list.selected_value()
        if student_selected is not None:
            self.event.emit(StudentViewModel.NavigateToMissScreen(student_selected))

    def get_student_list(self) -> LiveData[list[Student]]:
        return self._student_list.list_livedata()

    def get_student_index(self) -> LiveData[int]:
        return self._student_list.index_livedata()

    def get_selected_student(self) -> LiveData[Student | None]:
        return self._student_list.selected_livedata()
