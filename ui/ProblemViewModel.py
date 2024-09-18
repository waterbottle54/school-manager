from PyQt5.QtCore import QObject, pyqtSignal
from common.LiveData import *
from data.common.ListRepository import *
from data.common.ListDictRepository import *
from data.Problem import *
from data.BookRepository import *
from data.ProblemRepository import *
from data.ChapterRepository import *
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

    event: pyqtSignal = pyqtSignal(Event)

    book_repository: BookRepository
    chapter_repository: ChapterRepository
    problem_repository: ProblemRepository

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

    def __init__(self):
        super().__init__()
        self.book_repository = BookRepository()
        self.chapter_repository = ChapterRepository()
        self.problem_repository = ProblemRepository()

        self.book_list = self.book_repository.get_list()
        self.current_book_index = MutableLiveData(-1)
        self.current_book = map(self.current_book_index, lambda i: self.book_list[i] if i != -1 else None)

        self.grade_list = [ i for i in range(6, 12)]

        self.current_grade_index = MutableLiveData(-1)
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

    def on_resume(self):
        pass

    def on_book_change(self, index):
        self.current_book_index.set_value(index)

    def on_grade_change(self, index):
        self.current_grade_index.set_value(index)

    def on_chapter_change(self, index):
        self.current_chapter_index.set_value(index)

    def on_add_problem_click(self):
        grade = self.current_grade.value
        chapter = self.current_chapter.value
        book = self.current_book.value
        self.event.emit(ProblemViewModel.PromptProblemHeader(grade, chapter, book))

    def on_problem_header_result(self, problem_header: ProblemHeader):
        if problem_header is None:
            return
        print(problem_header.grade, problem_header.chapter, problem_header.book, problem_header.title)

    def on_delete_problem_click(self):
        pass