from PyQt5.QtCore import QObject, pyqtSignal
from common.LiveData import *

class StudentViewModel(QObject):

    class Event:
        pass

    event: pyqtSignal = pyqtSignal(Event)

    def __init__(self):
        super().__init__()
        
    def on_resume(self):
        pass
