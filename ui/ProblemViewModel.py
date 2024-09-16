from PyQt5.QtCore import QObject, pyqtSignal
from common.LiveData import *
from data.common.ListRepository import *
from data.common.ListDictRepository import *
from data.Problem import *
from data.ProblemRepository import *

class ProblemViewModel(QObject):

    class Event:
        pass

    class ConfirmDeleteProblem(Event):
        problem: Problem
        def __init__(self, problem: Problem):
            self.problem = problem

    event: pyqtSignal = pyqtSignal(Event)

    problem_repository: ProblemRepository

    def __init__(self):
        super().__init__()
        self.student_repository = ProblemRepository()

    def on_resume(self):
        pass