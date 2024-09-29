from PyQt5.QtCore import QObject, pyqtSignal
from common.LiveData import *
from data.ProblemRepository import *
from data.Student import *

class MissViewModel(QObject):

    class Event:
        pass

    class PromptProblemHeader(Event):
        student: Student
        def __init__(self, student):
            self.student = student

    class 

    event: pyqtSignal = pyqtSignal(Event)

    problem_repository: ProblemRepository

    student: Student


    def __init__(self):
        super().__init__()
        self.problem_repository = ProblemRepository()

    def on_start(self, arguments: dict):
        self.student = arguments['student']
        
    def on_result(self, data: dict):
        if data is not None:
            pass
    
    def on_add_miss_click(self):
        self.event.emit(MissViewModel.PromptProblemHeader())

    def on_problem_header_result(self, header: ProblemHeader):
        if header is None:
            return
        
        problem_existing = self.problem_repository.query_by_header(header)
        if len(problem_existing) > 0:
            problem = problem_existing[0]
            print(problem.to_record())
            # TODO: add miss to repository
        else:
            self.event.emit()