from PyQt5.QtCore import QObject, pyqtSignal
from common.LiveData import *
from data.common.ListRepository import *
from data.common.ListDictRepository import *
from data.Problem import *
from data.BookRepository import *
from data.ProblemRepository import *
from data.ChapterRepository import *

class AddProblemViewModel(QObject):

    class Event:
        pass

    event: pyqtSignal = pyqtSignal(Event)

    def __init__(self):
        super().__init__()
    
    def on_resume(self):
        pass

    def on_upload_picture_1_click(self):
        pass
        