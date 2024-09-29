from PyQt5.QtCore import QObject, pyqtSignal
from common.LiveData import *
from data.common.ListRepository import *
from data.common.ListDictRepository import *
from data.Problem import *
from data.BookRepository import *
from data.ProblemRepository import *
from data.ChapterRepository import *
from data.ImageRepository import *
from data.ProblemHeader import *

class ProblemViewModel(QObject):

    class Event:
        pass

    class PromptProblemHeader(Event):
        grade: int
        chapter: str
        book: str
        def __init__(self, grade: int, chapter: str, book: str):
            self.grade = grade
            self.chapter = chapter
            self.book = book

    class ConfirmDeleteProblem(Event):
        problem: Problem
        def __init__(self, problem: Problem):
            self.problem = problem

    class NavigateToAddProblem(Event):
        problem_header: ProblemHeader
        def __init__(self, header: ProblemHeader) -> None:
            super().__init__()
            self.problem_header = header

    class ShowGeneralMessage(Event):
        message: str
        def __init__(self, message: str):
            self.message = message

    event: pyqtSignal = pyqtSignal(Event)

    book_repository: BookRepository
    chapter_repository: ChapterRepository
    problem_repository: ProblemRepository
    image_repository: ImageRepository

    book_list: list
    current_book_index: MutableLiveData
    current_book: LiveData

    grade_list: list
    current_grade_index: MutableLiveData
    current_grade: LiveData

    chapter_list: LiveData
    current_chapter_index: MutableLiveData
    current_chapter: LiveData

    problem_list: LiveData
    current_problem_index: MutableLiveData
    current_problem: LiveData
    can_delete_problem: LiveData
    can_modify_problem: LiveData

    image_main: LiveData
    image_sub: LiveData

    range_num_choice: range

    def __init__(self):
        super().__init__()
        self.book_repository = BookRepository()
        self.chapter_repository = ChapterRepository()
        self.problem_repository = ProblemRepository()
        self.image_repository = ImageRepository()

        self.book_list = self.book_repository.get_list()
        self.current_book_index = MutableLiveData(0)
        self.current_book = map(self.current_book_index, lambda i: self.book_list[i] if i != -1 else None)

        self.grade_list = [ i for i in range(6, 12)]

        self.current_grade_index = MutableLiveData(2)
        self.current_grade = map(self.current_grade_index, 
                                 lambda i: self.grade_list[i] if i != -1 else None)

        self.chapter_list = map(self.current_grade, 
                                lambda grade: self.chapter_repository.get_list(grade) if grade is not None else [])
        
        self.current_chapter_index = MutableLiveData(-1)
        self.current_chapter = map2(self.chapter_list, self.current_chapter_index, 
                                 lambda chapters, i: chapters[i] if i > -1 and i < len(chapters) else None)
        
        self.problem_list = map3(self.current_book, self.current_grade, self.current_chapter,
                                 lambda book, grade, chapter: self.problem_repository.query(book, grade, chapter) 
                                 if None not in (book, grade, chapter) else [])
        
        self.current_problem_index = MutableLiveData(-1)
        self.current_problem = map2(self.problem_list, self.current_problem_index,
                                    lambda problems, i: problems[i] if i > -1 and i < len(problems) else None)
        self.can_delete_problem = map(self.current_problem, lambda problem: problem is not None)
        self.can_modify_problem = map(self.current_problem, lambda problem: problem is not None)

        self.image_main = map(self.current_problem,
                            lambda problem: self.image_repository.load_problem_image(from_problem(problem), True) 
                            if problem is not None else None)
        
        self.image_sub = map(self.current_problem,
                        lambda problem: self.image_repository.load_problem_image(from_problem(problem), False) 
                        if problem is not None else None)

        self.range_num_choice = range(3, 9)

    def on_resume(self):
        self.current_chapter_index.publish()

    def on_problem_click(self, row, column):
        self.current_problem_index.set_value(row)

    def on_book_change(self, index):
        self.current_book_index.set_value(index)
        self.current_problem_index.set_value(-1)

    def on_grade_change(self, index):
        self.current_grade_index.set_value(index)
        self.current_problem_index.set_value(-1)

    def on_chapter_change(self, index):
        self.current_chapter_index.set_value(index)
        self.current_problem_index.set_value(-1)

    def on_add_problem_click(self):
        grade = self.current_grade.value
        chapter = self.current_chapter.value
        book = self.current_book.value
        self.event.emit(ProblemViewModel.PromptProblemHeader(grade, chapter, book))

    def on_problem_header_result(self, problem_header: ProblemHeader):
        if problem_header is None:
            return
        existing = self.problem_repository.query_by_header(problem_header)
        if len(existing) == 0:
            self.event.emit(ProblemViewModel.NavigateToAddProblem(problem_header))
        else:
            self.event.emit(ProblemViewModel.ShowGeneralMessage('이미 등록되어 있는 문제입니다'))

    def on_delete_problem_click(self):
        if self.can_delete_problem.value is False:
            return
        self.event.emit(ProblemViewModel.ConfirmDeleteProblem(self.current_problem.value))

    def on_delete_probem_confirmed(self, problem: Problem):
        self.problem_repository.delete(problem.id)
        self.current_chapter_index.publish()

    def on_modify_problem_click(self):
        problem = self.current_problem.value
        if problem is not None:
            header = from_problem(problem)
            self.event.emit(ProblemViewModel.NavigateToAddProblem(header))