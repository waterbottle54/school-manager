from data.common.ListRepository import *
from common.Utils import *
from data.common.LiveData import *
from data.Student import *
from data.BookRepository import *
from data.ProblemRepository import *
from data.ChapterRepository import *


class PromptProblemHeaderViewModel:

    def __init__(
        self, init_grade: int | None, init_chapter: str | None, init_book: str | None
    ):
        super().__init__()

        self.init_chapter = init_chapter
        self.grade_list = [i for i in range(6, 12)]
        self.current_title = MutableLiveData("")

        self.book_repository = BookRepository.get_instance()
        self.chapter_repository = ChapterRepository.get_instance()
        self.problem_repository = ProblemRepository.get_instance()

        self.book_list = self.book_repository.get_list()
        self.current_book_index = MutableLiveData(-1)
        self.current_book = map(
            self.current_book_index,
            lambda i: (
                self.book_list[i] if (i > -1) and (i < len(self.book_list)) else None
            ),
        )

        self.current_grade_index = MutableLiveData(-1)
        self.current_grade = map(
            self.current_grade_index,
            lambda i: (
                self.grade_list[i] if (i > -1) and (i < len(self.grade_list)) else None
            ),
        )

        self.chapter_list = map(
            self.current_grade,
            lambda grade: (
                self.chapter_repository.get_list_by_key(grade)
                if grade is not None
                else []
            ),
        )

        self.current_chapter_index = MutableLiveData(-1)
        self.current_chapter = map2(
            self.chapter_list,
            self.current_chapter_index,
            lambda chapters, i: (
                chapters[i] if (i > -1) and (i < len(chapters)) else None
            ),
        )

        self.is_input_valid = map4(
            self.current_grade,
            self.current_book,
            self.current_chapter,
            self.current_title,
            lambda grade, book, chapter, title: None not in (grade, book, chapter)
            and len(title) > 0,
        )

        if init_grade in self.grade_list:
            i = self.grade_list.index(init_grade)
            self.current_grade_index.set_value(i)

        if init_book in self.book_list:
            i = self.book_list.index(init_book)
            self.current_book_index.set_value(i)

    def on_tick(self):
        _chapter_list = self.chapter_list.value
        if _chapter_list is not None and self.init_chapter in _chapter_list:
            i = _chapter_list.index(self.init_chapter)
            self.current_chapter_index.set_value(i)

    def on_grade_change(self, i: int):
        if (i >= 0) and (i < len(self.grade_list)):
            self.current_grade_index.set_value(i)

    def on_chapter_change(self, i: int):
        c_list = self.chapter_list.value
        if (c_list is not None) and (i >= 0) and (i < len(c_list)):
            self.current_chapter_index.set_value(i)

    def on_book_change(self, i: int):
        if (i >= 0) and (i < len(self.book_list)):
            self.current_book_index.set_value(i)

    def on_title_change(self, title: str):
        self.current_title.set_value(title.strip())
