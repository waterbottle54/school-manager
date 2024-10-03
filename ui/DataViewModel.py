from PyQt5.QtCore import QObject, pyqtSignal

from common.LiveData import *
from data.ChapterRepository import *
from data.SchoolRepository import *
from data.BookRepository import *


class DataViewModel(QObject):

    class Event:
        pass

    class NavigateBack(Event):
        pass

    class PromptSchoolName(Event):
        pass

    class PromptBookName(Event):
        pass

    class PromptChapterName(Event):
        grade: int

        def __init__(self, _grade):
            super().__init__()
            self.grade = _grade

    event: pyqtSignal = pyqtSignal(Event)

    school_repository: SchoolRepository
    book_repository: BookRepository
    chapter_repository: ChapterRepository

    """
    chapter_dict is dictionary,
    because chapter data is stored in file like below:
    {
        '0': ['ch0-1', 'ch0-2'],
        '1': ['ch1-1', 'ch1-2'],
        ...
    }
    where '0', '1' is zero-based grade, 
    and [] is chapters in each grade,
    """
    school_list: MutableLiveData[list[str]]
    book_list: MutableLiveData[list[str]]
    chapter_dict: MutableLiveData[dict[int, list[str]]]
    chapter_list: LiveData[list[str]]

    school_index: MutableLiveData[int]
    book_index: MutableLiveData[int]
    chapter_index: MutableLiveData[int]

    current_grade: MutableLiveData[int]
    current_school: LiveData[str | None]
    current_book: LiveData[str | None]
    current_chapter: LiveData[str | None]

    can_move_chapter_left: LiveData[bool]
    can_move_chapter_right: LiveData[bool]

    def __init__(self):
        super().__init__()

        self.school_repository = SchoolRepository()
        self.book_repository = BookRepository()
        self.chapter_repository = ChapterRepository()

        self.school_list = MutableLiveData([])
        self.book_list = MutableLiveData([])
        self.chapter_dict = MutableLiveData({})

        self.school_index = MutableLiveData(-1)
        self.book_index = MutableLiveData(-1)
        self.chapter_index = MutableLiveData(-1)

        self.current_grade = MutableLiveData(-1)
        self.current_school = map2(
            self.school_list,
            self.school_index,
            lambda list, i: list[i] if (i >= 0) and (i <= len(list) - 1) else None,
        )
        self.current_book = map2(
            self.book_list,
            self.book_index,
            lambda list, i: list[i] if (i >= 0) and (i <= len(list) - 1) else None,
        )
        self.chapter_list = map2(
            self.chapter_dict,
            self.current_grade,
            lambda dict, grade: (
                dict[grade] if (grade in dict) and (grade != -1) else []
            ),
        )

        self.can_move_chapter_left = map(self.chapter_index, lambda i: i > 0)
        self.can_move_chapter_right = map(
            self.chapter_index,
            lambda i: (i > -1) and (i < len(self.chapter_list.value) - 1),
        )

    def on_start(self):
        self._update_book_list()
        self._update_school_list()
        self._update_chapter_dict()

    def on_back_click(self):
        self.event.emit(DataViewModel.NavigateBack())

    def on_school_click(self, index):
        self.school_index.set_value(index)

    def on_add_school_click(self):
        self.event.emit(DataViewModel.PromptSchoolName())

    def on_add_school_result(self, school_name):
        self.school_repository.add_item(school_name)
        self._update_school_list()

    def on_delete_school_click(self):
        current_scool = self.current_school.value
        if current_scool is not None:
            self.school_repository.delete_item(current_scool)
            self._update_school_list()

    def on_book_click(self, index):
        self.book_index.set_value(index)

    def on_add_book_click(self):
        self.event.emit(DataViewModel.PromptBookName())

    def on_add_book_result(self, book_name):
        self.book_repository.add_item(book_name)
        self._update_book_list()

    def on_delete_book_click(self):
        current_book = self.current_book.value
        if current_book is not None:
            self.book_repository.delete_item(current_book)
            self._update_book_list()

    def on_add_chapter_click(self):
        if self.current_grade != -1:
            self.event.emit(DataViewModel.PromptChapterName(self.current_grade))

    def on_add_chapter_result(self, chapter_name):
        current_grade = self.current_grade.value
        if current_grade != -1:
            chapter_index = self.chapter_index.value
            self.chapter_repository.insert_item(
                current_grade, chapter_name, chapter_index + 1
            )
            self._update_chapter_dict()

    def on_delete_chapter_click(self):
        current_chapter = self.current_chapter.value
        if current_chapter is not None:
            grade = self.current_grade.value
            index = self.chapter_index.value
            self.chapter_repository.delete_item(grade, current_chapter)
            self._update_chapter_dict()

    def on_chapter_click(self, index):
        self.chapter_index.set_value(index)

    def on_chapter_up_click(self):
        if self.can_move_chapter_left.value:
            grade = self.current_grade.value
            index = self.chapter_index.value
            self.chapter_repository.move_item_left(grade, index)
            self._update_chapter_dict()

    def on_chapter_down_click(self):
        if self.can_move_chapter_right.value is True:
            grade = self.current_grade.value
            index = self.chapter_index.value
            self.chapter_repository.move_item_right(grade, index)
            self._update_chapter_dict()

    def on_grade_change(self, grade):
        self.current_grade.set_value(grade)

    def _update_school_list(self):
        s_list = self.school_repository.get_list()
        self.school_list.set_value(s_list)

    def _update_book_list(self):
        b_list = self.book_repository.get_list()
        self.book_list.set_value(b_list)

    def _update_chapter_dict(self):
        c_dict = self.chapter_repository.get_dict()
        self.chapter_dict.set_value(c_dict)
