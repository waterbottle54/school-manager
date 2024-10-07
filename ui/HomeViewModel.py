from PyQt5.QtCore import QObject, pyqtSignal
from common.LiveData import *


class HomeViewModel(QObject):

    class Event:
        pass

    class NavigateToAdminScreen(Event):
        pass

    event: pyqtSignal = pyqtSignal(Event)

    def __init__(self):
        super().__init__()

    def on_name_change(self, name: str):
        if len(name) > 0:
            self.event.emit(HomeViewModel.NavigateToAdminScreen())
