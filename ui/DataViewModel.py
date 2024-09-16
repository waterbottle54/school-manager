from PyQt5.QtCore import QObject, pyqtSignal
from common.LiveData import *
from data.common.ListRepository import *
from data.common.ListDictRepository import *

class DataViewModel(QObject):

    class Event:
        pass

    class NavigateBack(Event):
        pass

    class PromptSchoolName(Event):
        pass

    class PromptBookName(Event):
        pass

    class PromptChapterName(Event):
        grade: int
        def __init__(self, _grade):
            super().__init__()
            self.grade = _grade

    event: pyqtSignal = pyqtSignal(Event)
    
    school_repository: ListRepository
    book_repository: ListRepository
    chapter_repository: ListDictRepository

    school_list: MutableLiveData
    book_list: MutableLiveData
    chapter_list: MutableLiveData

    current_school_index: MutableLiveData
    current_book_index: MutableLiveData

    current_grade = -1
    current_chapter_index: MutableLiveData
    can_chapter_go_head: MutableLiveData
    can_chapter_go_tail: MutableLiveData

    def __init__(self):
        super().__init__()
        self.school_repository = ListRepository('school.json')
        self.book_repository = ListRepository('book.json')
        self.chapter_repository = ListDictRepository('chapter.json')
        self.school_list = MutableLiveData(list())
        self.book_list =  MutableLiveData(list())
        self.chapter_list = MutableLiveData(dict())
        self.current_school_index = MutableLiveData(-1)
        self.current_book_index = MutableLiveData(-1)
        self.current_chapter_index = MutableLiveData(-1)
        self.can_chapter_go_head = map(self.current_chapter_index, lambda i: i > 0)
        self.can_chapter_go_tail = map(self.current_chapter_index, lambda i: i > -1 and i < len(self.chapter_list.value) - 1)

    def on_resume(self):
        self.update_school()
        self.update_book()

    def on_back_click(self):
        self.event.emit(DataViewModel.NavigateBack())

    def on_school_click(self, index):
        self.current_school_index.set_value(index)

    def on_add_school_click(self):
        self.event.emit(DataViewModel.PromptSchoolName())

    def on_add_school_result(self, school_name):
        self.school_repository.add_item(school_name)
        self.update_school()

    def on_delete_school_click(self):
        index = self.current_school_index.value
        if index < 0 and index > len(self.school_list.value) - 1:
            return
        self.school_repository.delete_item(self.school_list.value[index])
        new_size = len(self.school_list.value) - 1
        self.update_school(index if index < new_size else index - 1)

    def on_book_click(self, index):
        self.current_book_index.set_value(index)

    def on_add_book_click(self):
        self.event.emit(DataViewModel.PromptBookName())

    def on_add_book_result(self, book_name):
        self.book_repository.add_item(book_name)
        self.update_book()

    def on_delete_book_click(self):
        index = self.current_book_index.value
        if index < 0 or index > len(self.book_list.value) - 1:
            return
        self.book_repository.delete_item(self.book_list.value[index])
        new_size = len(self.book_list.value) - 1
        self.update_book(index if index < new_size else index - 1)

    def on_add_chapter_click(self):
        if self.current_grade != -1:
            self.event.emit(DataViewModel.PromptChapterName(self.current_grade))

    def on_add_chapter_result(self, chapter_name):
        if self.current_grade != -1:
            chapter_index = self.current_chapter_index.value
            self.chapter_repository.insert_item(self.current_grade, chapter_name, chapter_index + 1)
            self.update_chapter(chapter_index + 1)

    def on_delete_chapter_click(self):
        index = self.current_chapter_index.value
        if index < 0 or index > len(self.chapter_list.value) - 1 or self.current_grade == -1:
            return
        self.chapter_repository.delete_item(self.current_grade, self.chapter_list.value[index])
        new_size = len(self.chapter_list.value) - 1
        self.update_chapter(index if index < new_size else index - 1)

    def on_chapter_click(self, index):
        self.current_chapter_index.set_value(index)

    def on_chapter_up_click(self):
        if self.current_grade == -1 or self.can_chapter_go_head.value is False:
            return
        index = self.current_chapter_index.value
        self.chapter_repository.move_item_up(self.current_grade, index)
        self.update_chapter(index - 1)
        
    def on_chapter_down_click(self):
        if self.current_grade == -1 or self.can_chapter_go_tail.value is False:
            return
        index = self.current_chapter_index.value
        self.chapter_repository.move_item_down(self.current_grade, index)
        self.update_chapter(index + 1)
        
    def on_grade_change(self, grade):
        self.current_grade = grade
        self.update_chapter(len(self.chapter_list.value) - 1)

    def update_school(self, index = None):
        schools = self.school_repository.get_list()
        self.school_list.set_value(schools)
        if index != None:
            self.current_school_index.set_value(index)
        else:
            self.current_school_index.publish()

    def update_book(self, index = None):
        books = self.book_repository.get_list()
        self.book_list.set_value(books)
        if index != None:
            self.current_book_index.set_value(index)
        else:
            self.current_book_index.publish()

    def update_chapter(self, index = None):
        if self.current_grade == -1:
            return
        chapters = self.chapter_repository.get_list(self.current_grade)
        self.chapter_list.set_value(chapters)
        if index != None:
            self.current_chapter_index.set_value(index)
        else:
            self.current_chapter_index.publish()
