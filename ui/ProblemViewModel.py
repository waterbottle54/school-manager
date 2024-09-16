from PyQt5.QtCore import QObject, pyqtSignal
from common.LiveData import *
from data.common.ListRepository import *
from data.common.ListDictRepository import *
from data.Problem import *
from data.ProblemRepository import *
from data.ChapterRepository import *

class ProblemViewModel(QObject):

    class Event:
        pass

    class ConfirmDeleteProblem(Event):
        problem: Problem
        def __init__(self, problem: Problem):
            self.problem = problem

    event: pyqtSignal = pyqtSignal(Event)

    problem_repository: ProblemRepository
    chapter_repository: ChapterRepository

    grade_list: list
    current_grade_idx: MutableLiveData
    current_grade: LiveData

    chapter_list: LiveData
    current_chapter_index: MutableLiveData
    current_chapter: LiveData

    def __init__(self):
        super().__init__()
        self.problem_repository = ProblemRepository()
        self.chapter_repository = ChapterRepository()

        self.grade_list = [ i for i in range(6, 12)]

        self.current_grade_idx = MutableLiveData(-1)
        self.current_grade = map(self.current_grade_idx, 
                                 lambda i: self.grade_list[i] if i != -1 else None)

        self.chapter_list = map(self.current_grade, 
                                lambda grade: self.chapter_repository.get_list(grade) if grade is not None else [])
        
        self.current_chapter_index = MutableLiveData(-1)
        self.current_chapter = map2(self.chapter_list, self.current_chapter_index, 
                                 lambda chapters, i: chapters[i] if i > -1 and i < len(chapters) else None)

    def on_resume(self):
        pass

    def on_grade_change(self, index):
        self.current_grade_idx.set_value(index)