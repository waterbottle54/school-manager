from PyQt5.QtWidgets import QSizePolicy, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QInputDialog, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from ui.common.Fragment import *
from ui.DataViewModel import *
from common.StringRes import *
import numpy as np
from PyQt5.QtCore import QTimer

class DataFragment(Fragment):

    view_model: DataViewModel

    layout: QVBoxLayout
    layout_school: QVBoxLayout
    layout_book: QVBoxLayout
    layout_chapter: QVBoxLayout

    lw_school: QListWidget
    lw_book: QListWidget
    lw_chapter: QListWidget
    cb_grade: QComboBox

    def __init__(self, title, view_model):
        super().__init__(title)

        self.view_model = view_model
        
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.layout_school = QVBoxLayout()
        self.layout_book = QVBoxLayout()
        self.layout_chapter = QVBoxLayout()

        self.layout.addLayout(self.layout_school)
        self.layout.addLayout(self.layout_book)
        self.layout.addLayout(self.layout_chapter)

        self.setup_school_sector()
        self.setup_book_sector()
        self.setup_chapter_sector()

        self.view_model.on_grade_change(0)

        self.view_model.school_list.observe(self.update_school_lw)
        self.view_model.book_list.observe(self.update_book_lw)
        self.view_model.chapter_list.observe(self.update_chapter_lw)

        self.view_model.current_school_index.observe(lambda i: self.update_school_selection(i))
        self.view_model.current_book_index.observe(lambda i: self.update_book_selection(i))
        self.view_model.current_chapter_index.observe(lambda i: self.button_remove_chapter.setEnabled(i != -1))
        self.view_model.current_chapter_index.observe(lambda i: QTimer.singleShot(10, lambda: self.update_chapter_selection(i)))
        self.view_model.can_chapter_go_head.observe(lambda can: self.button_chapter_up.setEnabled(can))
        self.view_model.can_chapter_go_tail.observe(lambda can: self.button_chapter_down.setEnabled(can))

        self.view_model.event.connect(self.on_event)

    def on_resume(self):
        self.view_model.on_resume()

    def on_event(self, event):
        if isinstance(event, DataViewModel.PromptSchoolName):
            self.prompt_school_name()
        if isinstance(event, DataViewModel.PromptBookName):
            self.prompt_book_name()
        if isinstance(event, DataViewModel.PromptChapterName):
            self.prompt_chapter_name(event.grade)

    def on_remove_school_click(self):
        self.view_model.on_delete_school_click()  

    def on_remove_book_click(self):
         self.view_model.on_delete_book_click()

    def on_remove_chapter_click(self):
        self.view_model.on_delete_chapter_click()

    def update_school_lw(self, schools):
        self.lw_school.clear()
        self.lw_school.addItems(schools)

    def update_school_selection(self, index):
        self.button_remove_school.setEnabled(index != -1)

        if index < 0 or index >= self.lw_school.count():
            self.lw_school.clearSelection()
            return
        self.lw_school.setCurrentRow(index)
        self.lw_school.setFocus()

    def update_book_lw(self, books):
        self.lw_book.clear()
        self.lw_book.addItems(books)

    def update_book_selection(self, index):
        self.button_remove_book.setEnabled(index != -1)

        if index < 0 or index >= self.lw_book.count():
            self.lw_book.clearSelection()
            return
        self.lw_book.setCurrentRow(index)
        self.lw_book.setFocus()

    def update_chapter_lw(self, chapters):
        self.lw_chapter.clear()
        self.lw_chapter.addItems(chapters)

    def update_chapter_selection(self, index):
        if index < 0 or index >= self.lw_chapter.count():
            self.lw_chapter.clearSelection()
            return
        self.lw_chapter.setCurrentRow(index)
        self.lw_chapter.setFocus()

    def prompt_school_name(self):
        school_name, ok = QInputDialog.getText(self, '학교 추가', '학교명')
        if ok == True:
           self.view_model.on_add_school_result(school_name)

    def prompt_book_name(self):
        book_name, ok = QInputDialog.getText(self, '교재 추가', '교재명')
        if ok == True:
           self.view_model.on_add_book_result(book_name)

    def prompt_chapter_name(self, grade):
        chapter_name, ok = QInputDialog.getText(self, f'{of_grade(grade)} 단원 추가', '단원명')
        if ok == True:
            self.view_model.on_add_chapter_result(chapter_name)

    def setup_school_sector(self):
        title = QLabel('학교')
        self.layout_school.addWidget(title)
    
        self.lw_school = QListWidget()
        self.lw_school.itemClicked.connect(lambda: self.view_model.on_school_click(self.lw_school.currentRow()))
        self.layout_school.addWidget(self.lw_school)

        self.button_add_school = QPushButton('학교 추가')
        self.button_add_school.setObjectName("modify")
        self.button_add_school.clicked.connect(self.view_model.on_add_school_click)
        self.layout_school.addWidget(self.button_add_school)

        self.button_remove_school = QPushButton('학교 삭제')
        self.button_remove_school.setObjectName("modify")
        self.button_remove_school.clicked.connect(self.on_remove_school_click)
        self.layout_school.addWidget(self.button_remove_school)
    
    def setup_book_sector(self):
        title = QLabel('교재')
        self.layout_book.addWidget(title)

        self.lw_book = QListWidget()
        self.lw_book.itemClicked.connect(lambda: self.view_model.on_book_click(self.lw_book.currentRow()))
        self.layout_book.addWidget(self.lw_book)

        self.button_add_book = QPushButton('교재 추가')
        self.button_add_book.setObjectName("modify")
        self.button_add_book.clicked.connect(self.view_model.on_add_book_click)
        self.layout_book.addWidget(self.button_add_book)

        self.button_remove_book = QPushButton('교재 삭제')
        self.button_remove_book.setObjectName("modify")
        self.button_remove_book.clicked.connect(self.on_remove_book_click)
        self.layout_book.addWidget(self.button_remove_book)

    def setup_chapter_sector(self):
        title = QLabel('단원')
        
        self.layout_chapter.addWidget(title)

        self.cb_grade = QComboBox()
        titles_grade = [ of_grade(g) for g in np.arange(0, 12) ]
        self.cb_grade.addItems(titles_grade)
        self.cb_grade.currentIndexChanged.connect(lambda index: self.view_model.on_grade_change(index + 0))
        self.layout_chapter.addWidget(self.cb_grade)

        self.lw_chapter = QListWidget()
        self.lw_chapter.currentItemChanged.connect(lambda: self.view_model.on_chapter_click(self.lw_chapter.currentRow()))
        self.layout_chapter.addWidget(self.lw_chapter)

        self.updown_button_layout = QHBoxLayout()
        self.layout_chapter.addLayout(self.updown_button_layout)

        self.button_chapter_up = QPushButton('▲')
        self.button_chapter_up.setObjectName("modify")
        self.button_chapter_up.clicked.connect(self.view_model.on_chapter_up_click)
        self.updown_button_layout.addWidget(self.button_chapter_up)

        self.button_chapter_down = QPushButton('▼')
        self.button_chapter_down.setObjectName("modify")
        self.button_chapter_down.clicked.connect(self.view_model.on_chapter_down_click)
        self.updown_button_layout.addWidget(self.button_chapter_down)

        self.button_add_chapter = QPushButton('단원 추가')
        self.button_add_chapter.setObjectName("modify")
        self.button_add_chapter.clicked.connect(self.view_model.on_add_chapter_click)
        self.layout_chapter.addWidget(self.button_add_chapter)

        self.button_remove_chapter = QPushButton('단원 삭제')
        self.button_remove_chapter.setObjectName("modify")
        self.button_remove_chapter.clicked.connect(self.on_remove_chapter_click)
        self.layout_chapter.addWidget(self.button_remove_chapter)