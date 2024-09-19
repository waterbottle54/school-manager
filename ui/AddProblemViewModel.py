from PyQt5.QtCore import QObject, pyqtSignal
from common.LiveData import *
from data.common.ListRepository import *
from data.common.ListDictRepository import *
from data.Problem import *
from data.BookRepository import *
from data.ProblemRepository import *
from data.ChapterRepository import *
from common.StringRes import *

class AddProblemViewModel(QObject):

    class Event:
        pass

    class PromptImageFile(Event):
        sequence: int
        def __init__(self, sequence):
            self.sequence = sequence

    class MakeCopyImage(Event):
        image_path: str
        folder_name: str
        file_name: str
        def __init__(self, image_path, folder_name, file_name):
            self.image_path = image_path
            self.folder_name = folder_name
            self.file_name = file_name

    class NavigateBackWithResult(Event):
        pass

    event: pyqtSignal = pyqtSignal(Event)

    problem_repository: ProblemRepository

    problem_header: ProblemHeader

    full_title: MutableLiveData

    image_path_1: MutableLiveData
    image_path_2: MutableLiveData

    problem_type: MutableLiveData

    range_num_choice: range
    current_num_choices: MutableLiveData
    answer_list_mcq: MutableLiveData
    answer_dict_saq: MutableLiveData

    is_input_valid: LiveData


    def __init__(self):
        super().__init__()
        self.problem_repository = ProblemRepository()

        self.full_title = MutableLiveData("")
        self.image_path_1 = MutableLiveData(None)
        self.image_path_2 = MutableLiveData(None)
        self.problem_type = MutableLiveData(0)

        self.range_num_choice = range(3, 9)
        self.current_num_choices = MutableLiveData(5)
        self.answer_list_mcq = MutableLiveData([])
        self.answer_dict_saq = MutableLiveData({})

        self.is_input_valid = map3(self.problem_type, self.answer_list_mcq, self.answer_dict_saq,
                                   lambda type, mcq, saq: len(mcq) > 0 if type == 0 else len(saq) > 0)
    
    def on_resume(self):
        pass

    def on_problem_header_set(self, header: ProblemHeader):
        self.problem_header = header
        self.full_title.set_value(f"{header.book} {of_grade(header.grade)}-{header.chapter} prob.{header.title}")

    def on_select_picture_1_click(self):
        self.event.emit(AddProblemViewModel.PromptImageFile(0))
        
    def on_select_picture_2_click(self):
        self.event.emit(AddProblemViewModel.PromptImageFile(1))

    def on_image_result(self, sequence, image_path):
        if sequence == 0:
            self.image_path_1.set_value(image_path)
        elif sequence == 1:
            self.image_path_2.set_value(image_path)

        header = self.problem_header
        folder_name = f'image_prob/{header.book}_{of_grade(header.grade)}_{header.chapter}'
        file_name = f'{header.title}_{sequence}'

        self.event.emit(AddProblemViewModel.MakeCopyImage(image_path, folder_name, file_name))

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
        grade, chapter, book, title = header.grade, header.chapter, header.book, header.title

        num_choices = self.current_num_choices.value
        ans_mcq = self.answer_list_mcq.value
        ans_saq = self.answer_dict_saq.value
        problem = Problem(grade, chapter, book, title, num_choices, ans_mcq, ans_saq) 

        self.problem_repository.insert(problem)
        self.event.emit(AddProblemViewModel.NavigateBackWithResult())

    def on_cancel_click(self):
        pass