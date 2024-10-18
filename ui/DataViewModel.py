from PyQt5.QtCore import QObject, pyqtSignal

from data.common.LiveData import *
from data.common.LiveList import *
from data.ChapterRepository import *
from data.SchoolRepository import *
from data.BookRepository import *
from data.common.LiveList import LiveList


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

    def __init__(self):
        super().__init__()

        self._school_repository = SchoolRepository.get_instance()
        self._book_repository = BookRepository.get_instance()
        self._chapter_repository = ChapterRepository.get_instance()

        self._current_grade = MutableLiveData(-1)
        self._school_list = LiveList[str](self._school_repository.get_list_livedata())
        self._book_list = LiveList[str](self._book_repository.get_list_livedata())

        self._chapter_list_livedata = map2(
            self._chapter_repository.get_dict_livedata(),
            self._current_grade,
            lambda dict, grade: dict[grade] if (grade in dict) else [],
        )
        self._chapter_list = LiveList[str](self._chapter_list_livedata)

        self.can_move_chapter_left = map(
            self._chapter_list.index_livedata(), lambda i: i > 0
        )
        self.can_move_chapter_right = map(
            self._chapter_list.index_livedata(),
            lambda i: (i > -1) and (i < len(self._chapter_list.list_value()) - 1),
        )

    def on_back_click(self):
        self.event.emit(DataViewModel.NavigateBack())

    def on_school_click(self, index: int):
        self._school_list.select_at(index)

    def on_book_click(self, index: int):
        self._book_list.select_at(index)

    def on_chapter_click(self, index: int):
        self._chapter_list.select_at(index)

    def on_add_school_click(self):
        self.event.emit(DataViewModel.PromptSchoolName())

    def on_add_book_click(self):
        self.event.emit(DataViewModel.PromptBookName())

    def on_add_chapter_click(self):
        current_grade = self._current_grade.value
        if current_grade != -1:
            self.event.emit(DataViewModel.PromptChapterName(current_grade))

    def on_add_school_result(self, school_name: str):
        self._school_list.set_default_index_on_update(True, lambda _, i_end, i: i_end)
        self._school_repository.add_item(school_name)

    def on_add_book_result(self, book_name: str):
        self._book_list.set_default_index_on_update(True, lambda _, i_end, i: i_end)
        self._book_repository.add_item(book_name)

    def on_add_chapter_result(self, chapter_name: str):
        current_grade = self._current_grade.value
        if current_grade == -1:
            return
        chapter_index = self._chapter_list.index_value()
        self._chapter_list.set_default_index_on_update(
            True, lambda _, i_end, i: chapter_index + 1
        )
        self._chapter_repository.insert_item(
            current_grade, chapter_name, chapter_index + 1
        )

    def on_delete_school_click(self):
        selected = self._school_list.selected_value()
        if selected is not None:
            self._school_list.set_default_index_on_update(
                True, lambda _, i_end, i: i if i < i_end else i_end
            )
            self._school_repository.delete_item(selected)

    def on_delete_book_click(self):
        selected = self._book_list.selected_value()
        if selected is not None:
            self._book_list.set_default_index_on_update(
                True, lambda _, i_end, i: i if i < i_end else i_end
            )
            self._book_repository.delete_item(selected)

    def on_delete_chapter_click(self):
        current_chapter = self._chapter_list.selected_value()
        if current_chapter is not None:
            current_grade = self._current_grade.value
            self._chapter_list.set_default_index_on_update(
                True, lambda _, i_end, i: i if i < i_end else i_end
            )
            self._chapter_repository.delete_item(current_grade, current_chapter)

    def on_chapter_up_click(self):
        if self.can_move_chapter_left.value:
            grade = self._current_grade.value
            index = self._chapter_list.index_value()
            self._chapter_list.set_default_index_on_update(
                True, lambda _, i_end, i: i - 1
            )
            self._chapter_repository.move_item_left(grade, index)

    def on_chapter_down_click(self):
        if self.can_move_chapter_right.value is True:
            grade = self._current_grade.value
            index = self._chapter_list.index_value()
            self._chapter_list.set_default_index_on_update(
                True, lambda _, i_end, i: i + 1
            )
            self._chapter_repository.move_item_right(grade, index)

    def on_grade_change(self, grade: int):
        self._current_grade.set_value(grade)

    def school_list_live(self) -> LiveData[list[str]]:
        return self._school_list.list_livedata()

    def school_index_live(self) -> LiveData[int]:
        return self._school_list.index_livedata()

    def book_list_live(self) -> LiveData[list[str]]:
        return self._book_list.list_livedata()

    def book_index_live(self) -> LiveData[int]:
        return self._book_list.index_livedata()

    def chapter_list_live(self) -> LiveData[list[str]]:
        return self._chapter_list.list_livedata()

    def chapter_index_live(self) -> LiveData[int]:
        return self._chapter_list.index_livedata()

    def grade_live(self) -> LiveData[int]:
        return self._current_grade
