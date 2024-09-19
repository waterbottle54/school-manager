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

    event: pyqtSignal = pyqtSignal(Event)

    problem_header: ProblemHeader

    full_title: MutableLiveData

    image_path_1: MutableLiveData
    image_path_2: MutableLiveData

    problem_type: MutableLiveData

    range_num_choice: range
    current_num_choice: MutableLiveData


    def __init__(self):
        super().__init__()
        self.full_title = MutableLiveData("")
        self.image_path_1 = MutableLiveData(None)
        self.image_path_2 = MutableLiveData(None)
        self.problem_type = MutableLiveData(0)

        self.range_num_choice = range(3, 9)
        self.current_num_choice = MutableLiveData(5)
    
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
        self.current_num_choice.set_value(self.range_num_choice.start + num)

    def on_submit_click(self):
        pass

    def on_cancel_click(self):
        pass