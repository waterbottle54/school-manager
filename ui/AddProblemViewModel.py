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

    book_repository: BookRepository
    chapter_repository: ChapterRepository
    problem_repository: ProblemRepository

    book_list: list
    current_book_index: MutableLiveData
    current_book: LiveData

    grade_list: list
    current_grade_index: MutableLiveData
    current_grade: LiveData

    chapter_list: LiveData
    current_chapter_index: MutableLiveData
    current_chapter: LiveData

    problem_list: LiveData

    def __init__(self):
        super().__init__()

        