from PyQt5.QtCore import QObject, pyqtSignal

from common.LiveData import *
from data.Miss import *
from data.MissRepository import *
from data.Problem import *
from data.ProblemHeader import *
from data.ProblemRepository import *
from data.Student import *


class MissViewModel(QObject):

    class Event:
        pass

    class PromptProblemHeader(Event):
        student: Student

        def __init__(self, student):
            self.student = student

    class NavigationToAddProblemScreen(Event):
        problem_header: ProblemHeader

        def __init__(self, problem_header: ProblemHeader):
            self.problem_header = problem_header

    event: pyqtSignal = pyqtSignal(Event)

    miss_repository: MissRepository
    problem_repository: ProblemRepository

    student: Student|None
    miss_list: MutableLiveData

    def __init__(self):
        super().__init__()
        self.miss_repository = MissRepository()
        self.problem_repository = ProblemRepository()
        self.student = None
        self.miss_list = MutableLiveData([])

    def on_start(self, arguments: dict):
        self.student = arguments["student"]
        self.update_miss_list()

    def on_result(self, data: dict):
        if data is None:
            problem: Problem = data["problem"]
            miss = Miss(self.student.id, problem.id, header_from_problem(problem))
            print(str(miss.to_record()))
            self.miss_repository.insert(miss)
        self.update_miss_list()

    def on_add_miss_click(self):
        self.event.emit(MissViewModel.PromptProblemHeader(self.student))

    def on_problem_header_result(self, header: ProblemHeader):
        if header is None or self.student is None:
            return

        problem_existing = self.problem_repository.query_by_header(header)
        if len(problem_existing) > 0:
            problem: Problem = problem_existing[0]
            miss = Miss(self.student.id, problem.id, header_from_problem(problem))
            self.miss_repository.insert(miss)
            self.update_miss_list()
        else:
            self.event.emit(MissViewModel.NavigationToAddProblemScreen(header))

    def update_miss_list(self):
        if self.student is None:
            return
        self.miss_list.set_value(
            self.miss_repository.query_by_student_id(self.student.id)
        )
