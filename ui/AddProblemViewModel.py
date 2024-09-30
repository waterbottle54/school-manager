import base64

from PyQt5.QtCore import QObject, pyqtSignal

from common.LiveData import *
from data.BookRepository import *
from data.ChapterRepository import *
from data.common.ListDictRepository import *
from data.common.ListRepository import *
from data.ImageRepository import *
from data.Problem import *
from data.ProblemRepository import *


class AddProblemViewModel(QObject):

    class Event:
        pass

    class PromptImageFile(Event):
        is_main: bool

        def __init__(self, is_main: bool):
            self.is_main = is_main

    class ConfirmDeleteImage(Event):
        is_main: bool

        def __init__(self, is_main: bool):
            self.is_main = is_main

    class NavigateBackWithResult(Event):
        problem: Problem

        def __init__(self, problem: Problem):
            self.problem = problem

    class NavigateBack(Event):
        pass

    event: pyqtSignal = pyqtSignal(Event)

    problem_repository: ProblemRepository
    image_repository: ImageRepository

    problem_header: ProblemHeader
    problem_existing: Problem

    problem_type: MutableLiveData

    range_num_choice: range
    current_num_choices: MutableLiveData
    answer_list_mcq: MutableLiveData
    answer_dict_saq: MutableLiveData

    image_data_main: MutableLiveData
    image_data_sub: MutableLiveData

    is_input_valid: LiveData

    def __init__(self):
        super().__init__()
        self.problem_repository = ProblemRepository()
        self.image_repository = ImageRepository()

        self.problem_type = MutableLiveData(0)

        self.range_num_choice = range(3, 9)
        self.current_num_choices = MutableLiveData(5)
        self.answer_list_mcq = MutableLiveData([])
        self.answer_dict_saq = MutableLiveData({})

        self.image_data_main = MutableLiveData(None)
        self.image_data_sub = MutableLiveData(None)

        self.is_input_valid = map4(
            self.problem_type,
            self.answer_list_mcq,
            self.answer_dict_saq,
            self.image_data_main,
            lambda type, mcq, saq, img: (img is not None)
            and (len(mcq) > 0 if type == 0 else len(saq) > 0),
        )

    def on_start(self, arguments: dict):

        self.problem_header = arguments["problem_header"]
        problem = self.problem_repository.query_by_header(self.problem_header)
        self.problem_existing = problem[0] if len(problem) > 0 else None

        if self.problem_existing is None:
            self.current_num_choices.set_value(5)
            self.image_data_main.set_value(None)
            self.image_data_sub.set_value(None)
            self.answer_list_mcq.set_value([])
            self.answer_dict_saq.set_value({})
        else:
            problem = self.problem_existing
            self.current_num_choices.set_value(problem.num_choice)
            self.answer_list_mcq.set_value(problem.ans_mcq)
            self.answer_dict_saq.set_value(problem.ans_saq)
            self.problem_type.set_value(0 if len(problem.ans_mcq) > 0 else 1)
            image_main = self.image_repository.load_problem_image(
                self.problem_header, True
            )
            image_sub = self.image_repository.load_problem_image(
                self.problem_header, False
            )
            self.image_data_main.set_value(image_main)
            self.image_data_sub.set_value(image_sub)

    def on_select_image_click(self, is_main: bool):
        self.event.emit(AddProblemViewModel.PromptImageFile(is_main))

    def on_image_result(self, data: bytes, is_main: bool):
        image = self.image_data_main if is_main else self.image_data_sub
        image.set_value(data)

    def on_delete_image_click(self, is_main: bool):
        data = self.image_data_main if is_main else self.image_data_sub
        if data.value is not None:
            self.event.emit(AddProblemViewModel.ConfirmDeleteImage(is_main))

    def on_delete_image_confirm(self, is_main: bool):
        data = self.image_data_main if is_main else self.image_data_sub
        if data.value is not None:
            result = self.image_repository.delete_problem_image(
                self.problem_header, is_main
            )
            if result == True:
                data.set_value(None)

    def on_type_click(self, type):
        self.problem_type.set_value(type)

    def on_num_choice_change(self, num):
        self.current_num_choices.set_value(self.range_num_choice.start + num)

    def on_choice_change(self, list_checked):
        list_choice = []
        for choice in list_checked:
            if choice < self.current_num_choices.value:
                list_choice.append(choice)
        self.answer_list_mcq.set_value(list_choice)

    def on_submit_click(self):
        if self.is_input_valid.value is False:
            return

        header = self.problem_header
        grade, chapter, book, title = (
            header.grade,
            header.chapter,
            header.book,
            header.title,
        )
        image_main, image_sub = self.image_data_main.value, self.image_data_sub.value

        num_choices = self.current_num_choices.value
        ans_mcq = self.answer_list_mcq.value
        ans_saq = self.answer_dict_saq.value
        problem = Problem(grade, chapter, book, title, num_choices, ans_mcq, ans_saq)

        if self.problem_existing is None:
            self.problem_repository.insert(problem)
        else:
            problem.id = self.problem_existing.id
            problem.created = self.problem_existing.created
            self.problem_repository.update(problem)

        self.image_repository.save_problem_image(header, image_main, True)
        if image_sub is not None:
            self.image_repository.save_problem_image(header, image_sub, False)

        self.event.emit(AddProblemViewModel.NavigateBackWithResult(problem))

    def on_cancel_click(self):
        self.event.emit(AddProblemViewModel.NavigateBack())
