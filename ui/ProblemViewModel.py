from PyQt5.QtCore import QObject, pyqtSignal

from data.common.LiveData import *
from data.BookRepository import *
from data.ChapterRepository import *
from data.common.DictOfListRepository import *
from data.common.ListRepository import *
from data.ImageRepository import *
from data.Problem import *
from data.ProblemHeader import *
from data.ProblemRepository import *
from data.common.LiveList import LiveList, MutableLiveList


class ProblemViewModel(QObject):

    class Event:
        pass

    class PromptProblemHeader(Event):
        def __init__(self, grade: int, chapter: str, book: str):
            self.grade = grade
            self.chapter = chapter
            self.book = book

    class ConfirmDeleteProblem(Event):
        def __init__(self, problem: Problem):
            self.problem = problem

    class NavigateToAddProblem(Event):
        def __init__(self, header: ProblemHeader) -> None:
            super().__init__()
            self.problem_header = header

    class ShowGeneralMessage(Event):
        def __init__(self, message: str):
            self.message = message

    event: pyqtSignal = pyqtSignal(Event)

    def __init__(self):
        super().__init__()

        # Member variables declaration
        self._book_repository = BookRepository()
        self._chapter_repository = ChapterRepository()
        self._problem_repository = ProblemRepository.get_instance()
        self._image_repository = ImageRepository()

        self._book_list: LiveList[str]
        self._grade_list: MutableLiveList[int]
        self._chapter_list: LiveList[str]
        self._problem_list: LiveList[Problem]

        self.image_main: LiveData[bytes | None]
        self.image_sub: LiveData[bytes | None]

        self.can_delete_problem: LiveData[bool]
        self.can_modify_problem: LiveData[bool]
        self.range_num_choice = range(4, 8)
        # End of member variables declaration

        self._book_list = LiveList(self._book_repository.get_list_livedata())
        self._grade_list = MutableLiveList([i for i in range(0, 12)])

        chapter_list_livedata = map2(
            self._chapter_repository.get_dict_livedata(),
            self._grade_list.index_livedata(),
            lambda dict, grade: dict[grade] if grade in dict else [],
        )
        self._chapter_list = LiveList(chapter_list_livedata)

        problem_list_livedata = map3(
            self._book_list.selected_livedata(),
            self._grade_list.selected_livedata(),
            self._chapter_list.selected_livedata(),
            lambda book, grade, chapter: (
                []
                if (book is None) or (grade is None) or (chapter is None)
                else self._problem_repository.get_problems(book, grade, chapter)
            ),
        )
        self._problem_list = LiveList(problem_list_livedata)

        self.image_main = map(
            self._problem_list.selected_livedata(),
            lambda problem: (
                self._image_repository.load_problem_image(
                    ProblemHeader.from_problem(problem), True
                )
                if problem is not None
                else None
            ),
        )
        self.image_sub = map(
            self._problem_list.selected_livedata(),
            lambda problem: (
                self._image_repository.load_problem_image(
                    ProblemHeader.from_problem(problem), False
                )
                if problem is not None
                else None
            ),
        )

        self.can_delete_problem = map(
            self._problem_list.selected_livedata(), lambda problem: problem is not None
        )
        self.can_modify_problem = map(
            self._problem_list.selected_livedata(), lambda problem: problem is not None
        )

    def on_restart(self, problem: Problem):
        self._problem_list.select(problem)

    def on_problem_click(self, row: int, column: int):
        self._problem_list.select_at(row)

    def on_book_change(self, index):
        self._book_list.select_at(index)
        self._problem_list.select_at(0)

    def on_grade_change(self, index: int):
        self._grade_list.select_at(index)
        self._problem_list.select_at(0)

    def on_chapter_change(self, index: int):
        self._chapter_list.select_at(index)
        self._problem_list.select_at(0)

    def on_add_problem_click(self):
        grade = self._grade_list.selected_value()
        chapter = self._chapter_list.selected_value()
        book = self._book_list.selected_value()
        if (grade is not None) and (chapter is not None) and (book is not None):
            self.event.emit(ProblemViewModel.PromptProblemHeader(grade, chapter, book))

    def on_problem_header_result(self, problem_header: ProblemHeader | None):
        if problem_header is None:
            return
        exists = self._problem_repository.get_problem_by_header(problem_header)
        if not exists:
            self.event.emit(ProblemViewModel.NavigateToAddProblem(problem_header))
        else:
            self.event.emit(
                ProblemViewModel.ShowGeneralMessage("이미 등록되어 있는 문제입니다")
            )

    def on_delete_problem_click(self):
        problem = self._problem_list.selected_value()
        if problem is not None:
            self.event.emit(ProblemViewModel.ConfirmDeleteProblem(problem))

    def on_delete_problem_confirmed(self, problem: Problem):
        self._problem_list.set_default_index_on_update(
            True, lambda list, i_end, i: i if i < i_end else i_end
        )
        self._problem_repository.delete(problem.id)

    def on_modify_problem_click(self):
        problem = self._problem_list.selected_value()
        if problem is not None:
            header = ProblemHeader.from_problem(problem)
            self.event.emit(ProblemViewModel.NavigateToAddProblem(header))

    def grade_list(self) -> LiveData[list[int]]:
        return self._grade_list.list_livedata()

    def grade_index(self) -> LiveData[int]:
        return self._grade_list.index_livedata()

    def book_list(self) -> LiveData[list[str]]:
        return self._book_list.list_livedata()

    def book_index(self) -> LiveData[int]:
        return self._book_list.index_livedata()

    def chapter_list(self) -> LiveData[list[str]]:
        return self._chapter_list.list_livedata()

    def chapter_index(self) -> LiveData[int]:
        return self._chapter_list.index_livedata()

    def problem_list(self) -> LiveData[list[Problem]]:
        return self._problem_list.list_livedata()

    def problem_index(self) -> LiveData[int]:
        return self._problem_list.index_livedata()

    def problem_selected(self) -> LiveData[Problem | None]:
        return self._problem_list.selected_livedata()
