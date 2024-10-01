from PyQt5.QtCore import QObject, pyqtSignal

from common.LiveData import *
from data.Miss import *
from data.MissRepository import *
from data.Problem import *
from data.ProblemHeader import *
from data.ProblemRepository import *
from data.Student import *
from data.ImageRepository import *


class MissViewModel(QObject):

    class Event:
        pass

    class PromptProblemHeader(Event):
        student: Student
        def __init__(self, student: Student):
            self.student = student

    class NavigationToAddProblemScreen(Event):
        problem_header: ProblemHeader

        def __init__(self, problem_header: ProblemHeader):
            self.problem_header = problem_header

    class ConfirmDeleteMiss(Event):
        miss: Miss
        def __init__(self, miss: Miss):
            self.miss = miss

    event: pyqtSignal = pyqtSignal(Event)

    miss_repository: MissRepository
    problem_repository: ProblemRepository
    image_repository: ImageRepository

    student: Student|None

    miss_list: MutableLiveData
    current_miss_index: MutableLiveData
    current_miss: LiveData

    image_main: LiveData
    image_sub: LiveData

    can_delete_miss: LiveData
    can_modify_problem: LiveData

    def __init__(self):
        super().__init__()

        self.miss_repository = MissRepository()
        self.problem_repository = ProblemRepository()
        self.image_repository = ImageRepository()

        self.student = None
        self.miss_list = MutableLiveData([])
        self.current_miss_index = MutableLiveData(-1)

        self.current_miss = map2(
            self.miss_list, 
            self.current_miss_index,
            lambda list, i: 
                list[i] 
                if (list is not None) and (i >= 0) and (i < len(list))
                else None
        )

        self.image_main = map(
            self.current_miss,
            lambda miss: 
                self.image_repository.load_problem_image(miss.problem_header, True)
                if miss is not None
                else None
        )
        self.image_sub = map(
            self.current_miss,
            lambda miss:
                self.image_repository.load_problem_image(miss.problem_header, False)
                if miss is not None
                else None
        )

        self.can_delete_miss = map(self.current_miss, lambda miss: miss is not None)
        self.can_modify_problem = map(self.current_miss, lambda miss: miss is not None)

    def on_start(self, arguments: dict):
        self.student = arguments["student"]
        self._update_miss_list()

    def on_result(self, data: dict):
        if data is None:
            problem: Problem = data["problem"]
            miss = Miss(self.student.id, problem.id, ProblemHeader.from_problem(problem))
            print(str(miss.to_record()))
            self.miss_repository.insert(miss)
        self._update_miss_list()

    def on_miss_selected(self, row: int, column: int):
        self.current_miss_index.set_value(row)

    def on_add_miss_click(self):
        if self.student is not None:
            self.event.emit(MissViewModel.PromptProblemHeader(self.student))

    def on_delete_miss_click(self):
        if self.current_miss.value is not None:
            self.event.emit(MissViewModel.ConfirmDeleteMiss(self.current_miss.value))

    def on_delete_message_confirm(self, miss: Miss):
        self.miss_repository.delete(miss.id)
        self._update_miss_list()

    def on_problem_header_result(self, header: ProblemHeader):
        if header is None or self.student is None:
            return

        problem_existing = self.problem_repository.query_by_header(header)
        if len(problem_existing) > 0:
            problem: Problem = problem_existing[0]
            miss = Miss(self.student.id, problem.id, ProblemHeader.from_problem(problem))
            self.miss_repository.insert(miss)
            self._update_miss_list()
        else:
            self.event.emit(MissViewModel.NavigationToAddProblemScreen(header))

    def _update_miss_list(self):
        if self.student is not None:
            list = self.miss_repository.query_by_student_id(self.student.id)
            self.miss_list.set_value(list)
            if self.current_miss.value is None:
                self._reset_miss_index()

    def _reset_miss_index(self):
        list = self.miss_list.value
        if (list is None) or (len(list) == 0):
            self.current_miss_index.set_value(-1)
        else:
            self.current_miss_index.set_value(0)

