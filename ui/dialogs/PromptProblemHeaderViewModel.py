from data.common.ListRepository import *
from common.Utils import *
from common.LiveData import *
from data.Student import *
from data.BookRepository import *
from data.ProblemRepository import *
from data.ChapterRepository import *

class PromptProblemHeaderViewModel:

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

    current_title: MutableLiveData

    is_input_valid: LiveData
    init_chapter = None

    def __init__(self, init_grade, init_chapter, init_book):
        super().__init__()

        self.init_chapter = init_chapter

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
        
        self.current_title = MutableLiveData("")

        self.is_input_valid = map4(self.current_grade, self.current_book, self.current_chapter, self.current_title,
                                   lambda grade, book, chapter, title: None not in (grade, book, chapter) and len(title) > 0)

        if init_grade in self.grade_list:
            i = self.grade_list.index(init_grade)
            self.current_grade_index.set_value(i)
        
        if self.book_list is not None and init_book in self.book_list:
            i = self.book_list.index(init_book)
            self.current_book_index.set_value(i)

    def on_tick(self):
        _chapter_list = self.chapter_list.value
        if _chapter_list is not None and self.init_chapter in _chapter_list:
            i = _chapter_list.index(self.init_chapter)
            self.current_chapter_index.set_value(i)

    def on_grade_change(self, i):
        if i >= 0 and i < len(self.grade_list):
            self.current_grade_index.set_value(i)

    def on_chapter_change(self, i):
        list = self.chapter_list.value
        if list is not None and i >= 0 and i < len(list):
            self.current_chapter_index.set_value(i)

    def on_book_change(self, i):
        list = self.book_list
        if list is not None and i >= 0 and i < len(list):
            self.current_book_index.set_value(i)

    def on_title_change(self, text: str):
        self.current_title.set_value(text.strip())