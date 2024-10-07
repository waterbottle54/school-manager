from PyQt5.QtCore import QObject, pyqtSignal
from common.LiveData import *


class AdminViewModel(QObject):

    class Event:
        pass

    class NavigateBack(Event):
        pass

    class NavigateToDataFragment(Event):
        pass

    class NavigateToStudentFragment(Event):
        pass

    class NavigateToProblemFragment(Event):
        pass

    event: pyqtSignal = pyqtSignal(Event)

    def __init__(self):
        super().__init__()

    def on_back_click(self):
        self.event.emit(AdminViewModel.NavigateBack())

    def on_data_click(self):
        self.event.emit(AdminViewModel.NavigateToDataFragment())

    def on_student_click(self):
        self.event.emit(AdminViewModel.NavigateToStudentFragment())

    def on_problem_click(self):
        self.event.emit(AdminViewModel.NavigateToProblemFragment())
