from data.common.ListRepository import *
from common.Utils import *
from common.LiveData import *
import numpy as np
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
        
        self.current_title = MutableLiveData("")

        self.is_input_valid = map4(self.current_grade, self.current_book, self.current_chapter, self.current_title,
                                   lambda grade, book, chapter, title: None not in (grade, book, chapter) and len(title) > 0)

    def on_grade_change(self, i):
        if i >= 0 and i < len(self.grade_list):
            self.current_grade_index.set_value(self.grade_list[i])

    def on_chapter_change(self, i):
        list = self.chapter_list.value
        if list is not None and i >= 0 and i < len(list):
            self.current_chapter_index.set_value(list[i])

    def on_book_change(self, i):
        list = self.book_list.value
        if list is not None and i >= 0 and i < len(list):
            self.current_book_index.set_value(list[i])

    def on_title_change(self, text: str):
        self.current_title.set_value(text.strip())