from PyQt5.QtCore import QObject, pyqtSignal

from data.common.LiveData import *
from data.Miss import *
from data.MissRepository import *
from data.Problem import *
from data.ProblemHeader import *
from data.ProblemRepository import *
from data.Student import *
from data.ImageRepository import *
from data.common.LiveList import LiveList, MutableLiveList


class MissViewModel(QObject):

    class Event:
        pass

    class PromptProblemHeader(Event):
        def __init__(self, student: Student):
            self.student = student

    class NavigationToAddProblemScreen(Event):
        def __init__(self, problem_header: ProblemHeader):
            self.problem_header = problem_header

    class ConfirmDeleteMiss(Event):
        def __init__(self, miss: Miss):
            self.miss = miss

    event: pyqtSignal = pyqtSignal(Event)

    def __init__(self):
        super().__init__()

        self._miss_repository = MissRepository.get_instance()
        self._problem_repository = ProblemRepository.get_instance()
        self._image_repository = ImageRepository.get_instance()
        self._student = MutableLiveData[Student | None](None)
        self._miss_list: LiveList[Miss]
        self.image_main: LiveData[bytes | None]
        self.image_sub: LiveData[bytes | None]
        self.can_delete_miss: LiveData[bool]
        self.can_modify_problem: LiveData[bool]

        miss_list_livedata = map(
            self._student,
            lambda student: (
                self._miss_repository.get_misses_by_student_id(student.id)
                if student is not None
                else []
            ),
        )
        self._miss_list = LiveList(miss_list_livedata)

        self.image_main = map(
            self._miss_list.selected_livedata(),
            lambda miss: (
                self._image_repository.load_problem_image(miss.problem_header, True)
                if miss is not None
                else None
            ),
        )
        self.image_sub = map(
            self._miss_list.selected_livedata(),
            lambda miss: (
                self._image_repository.load_problem_image(miss.problem_header, False)
                if miss is not None
                else None
            ),
        )

        self.can_delete_miss = map(
            self._miss_list.selected_livedata(), lambda miss: miss is not None
        )
        self.can_modify_problem = map(
            self._miss_list.selected_livedata(), lambda miss: miss is not None
        )

    def on_start(self, arguments: dict[str, object] | None):
        self._student.set_value(None)
        if (arguments is not None) and ("student" in arguments):
            student = arguments["student"]
            if isinstance(student, Student):
                self._student.set_value(student)

    def on_result(self, result: dict[str, object] | None):
        student = self._student.value
        if student is None:
            return
        if (result is not None) and ("problem" in result):
            problem = result["problem"]
            if isinstance(problem, Problem):
                header = ProblemHeader.from_problem(problem)
                miss = Miss(student.id, problem.id, header)
                self._miss_repository.insert(miss)

    def on_miss_selected(self, row: int, column: int):
        self._miss_list.select_at(row)

    def on_add_miss_click(self):
        student = self._student.value
        if student is not None:
            self.event.emit(MissViewModel.PromptProblemHeader(student))

    def on_delete_miss_click(self):
        miss_selected = self._miss_list.selected_value()
        if miss_selected is not None:
            self.event.emit(MissViewModel.ConfirmDeleteMiss(miss_selected))

    def on_delete_message_confirm(self, miss: Miss):
        self._miss_repository.delete(miss.id)

    def on_problem_header_result(self, header: ProblemHeader | None):
        student = self._student.value
        if (header is None) or (student is None):
            return
        problem_existing = self._problem_repository.get_problem_by_header(header)
        if problem_existing is not None:
            header = ProblemHeader.from_problem(problem_existing)
            miss = Miss(student.id, problem_existing.id, header)
            self._miss_repository.insert(miss)
        else:
            self.event.emit(MissViewModel.NavigationToAddProblemScreen(header))

    def get_miss_list(self) -> LiveData[list[Miss]]:
        return self._miss_list.list_livedata()

    def get_miss_index(self) -> LiveData[int]:
        return self._miss_list.index_livedata()

    def get_selected_miss(self) -> LiveData[Miss | None]:
        return self._miss_list.selected_livedata()
