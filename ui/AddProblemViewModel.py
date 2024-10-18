import base64

from PyQt5.QtCore import QObject, pyqtSignal

from data.common.LiveData import *
from data.BookRepository import *
from data.ChapterRepository import *
from data.common.DictOfListRepository import *
from data.common.ListRepository import *
from data.ImageRepository import *
from data.Problem import *
from data.ProblemRepository import *


class AddProblemViewModel(QObject):

    class Event:
        pass

    class PromptImageFile(Event):
        def __init__(self, is_main: bool):
            self.is_main = is_main

    class ConfirmDeleteImage(Event):
        def __init__(self, is_main: bool):
            self.is_main = is_main

    class NavigateBackWithResult(Event):
        def __init__(self, problem_id: int):
            self.problem_id = problem_id

    class NavigateBack(Event):
        pass

    _event = pyqtSignal(Event)

    def __init__(self):
        super().__init__()
        self._problem_repository = ProblemRepository.get_instance()
        self._image_repository = ImageRepository.get_instance()
        self._problem_header: ProblemHeader | None = None
        self._problem_existing: Problem | None = None
        self.problem_type = MutableLiveData(0)
        self.range_num_choice = range(3, 9)
        self.current_num_choices = MutableLiveData(5)
        self.answer_list_mcq = MutableLiveData([])
        self.answer_dict_saq = MutableLiveData({})
        self.image_data_main = MutableLiveData[bytes | None](None)
        self.image_data_sub = MutableLiveData[bytes | None](None)
        self.is_input_valid: LiveData[bool]

        self.is_input_valid = map4(
            self.problem_type,
            self.answer_list_mcq,
            self.answer_dict_saq,
            self.image_data_main,
            lambda type, mcq, saq, img: (img is not None)
            and (len(mcq) > 0 if type == 0 else len(saq) > 0),
        )

    def on_start(self, arguments: dict[str, object] | None):
        if (arguments is not None) and ("problem_header" in arguments):
            problem_header = arguments["problem_header"]
            if (problem_header is not None) and isinstance(
                problem_header, ProblemHeader
            ):
                self._problem_header = problem_header
                self.on_header_changed(self._problem_header)

    def on_header_changed(self, header: ProblemHeader):
        problem = self._problem_repository.get_problem_by_header(header)
        self._problem_existing = problem

        if problem is None:
            # Adding new problem: Empty problem input data
            self.current_num_choices.set_value(5)
            self.image_data_main.set_value(None)
            self.image_data_sub.set_value(None)
            self.answer_list_mcq.set_value([])
            self.answer_dict_saq.set_value({})
        else:
            # Editing existing problem: Set problem input data accordingly
            self.current_num_choices.set_value(problem.num_choice)
            self.answer_list_mcq.set_value(problem.ans_mcq)
            self.answer_dict_saq.set_value(problem.ans_saq)
            self.problem_type.set_value(0 if len(problem.ans_mcq) > 0 else 1)
            image_main = self._image_repository.load_problem_image(header, True)
            image_sub = self._image_repository.load_problem_image(header, False)
            self.image_data_main.set_value(image_main)
            self.image_data_sub.set_value(image_sub)

    def on_select_image_click(self, is_main: bool):
        self._event.emit(AddProblemViewModel.PromptImageFile(is_main))

    def on_image_result(self, data: bytes, is_main: bool):
        image = self.image_data_main if is_main else self.image_data_sub
        image.set_value(data)

    def on_delete_image_click(self, is_main: bool):
        data = self.image_data_main if is_main else self.image_data_sub
        if data.value is not None:
            self.event.emit(AddProblemViewModel.ConfirmDeleteImage(is_main))

    def on_delete_image_confirmed(self, is_main: bool):
        if self._problem_header is None:
            return
        image_data = self.image_data_main if is_main else self.image_data_sub
        if image_data.value is not None:
            result = self._image_repository.delete_problem_image(
                self._problem_header, is_main
            )
            if result:
                image_data.set_value(None)

    def on_type_click(self, type):
        self.problem_type.set_value(type)

    def on_num_choice_change(self, num: int):
        self.current_num_choices.set_value(self.range_num_choice.start + num)

    def on_choice_changed(self, list_checked: list[int]):
        list_choice = []
        for choice in list_checked:
            if choice < self.current_num_choices.value:
                list_choice.append(choice)
        self.answer_list_mcq.set_value(list_choice)

    def on_submit_click(self):
        header = self._problem_header
        if (header is None) or (not self.is_input_valid.value):
            return

        image_main = self.image_data_main.value
        image_sub = self.image_data_sub.value
        if image_main is None:
            return

        num_choices = self.current_num_choices.value
        ans_mcq = self.answer_list_mcq.value
        ans_saq = self.answer_dict_saq.value
        problem = Problem(
            header.grade,
            header.chapter,
            header.book,
            header.title,
            num_choices,
            ans_mcq,
            ans_saq,
        )
        
        problem_id = -1
        if self._problem_existing is None:
            # Adding situation: Insert the problem
            self._problem_repository.insert(problem)
            added = self._problem_repository.get_problem_by_header(header)
            if added is not None:
                problem_id = added.id
        else:
            # Editing situation: Update the problem
            problem.id = self._problem_existing.id
            problem.created = self._problem_existing.created
            self._problem_repository.update(problem)
            problem_id = self._problem_existing.id

        # Save Image(s)
        self._image_repository.save_problem_image(header, image_main, True)
        if image_sub is not None:
            self._image_repository.save_problem_image(header, image_sub, False)

        if problem_id != -1:
            self._event.emit(AddProblemViewModel.NavigateBackWithResult(problem_id))
        
    def on_cancel_click(self):
        self._event.emit(AddProblemViewModel.NavigateBack())
