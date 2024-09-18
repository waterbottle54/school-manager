from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QComboBox,
                             QVBoxLayout, QHBoxLayout, QPushButton)
from PyQt5.QtCore import QTimer
from ui.dialogs.PromptProblemHeaderViewModel import *
from data.ProblemHeader import *
from common.StringRes import *

class PromptProblemHeaderDialog(QDialog):

    view_model: PromptProblemHeaderViewModel

    def __init__(self, init_grade, init_chapter, init_book):
        super().__init__()

        self.view_model = PromptProblemHeaderViewModel(init_grade, init_chapter, init_book)

        self.setWindowTitle("문제 입력")
        self.setup_ui()

        self.view_model.chapter_list.observe(self.update_chapter_combo)
        self.view_model.current_book_index.observe(self.combo_book.setCurrentIndex)
        self.view_model.current_grade_index.observe(self.combo_grade.setCurrentIndex)
        self.view_model.current_chapter_index.observe(self.combo_chapter.setCurrentIndex)
        self.view_model.is_input_valid.observe(self.button_submit.setEnabled)

        QTimer.singleShot(100, self.view_model.on_tick)

    def update_chapter_combo(self, chapters):
        self.combo_chapter.clear()
        self.combo_chapter.addItems(chapters)

        index = self.view_model.current_chapter_index.value
        if index is not None and index >= 0 and index < len(chapters):
            self.combo_chapter.setCurrentIndex(index)

    def update_chapter_combo_selection(self, i):
        self.combo_chapter.setCurrentIndex(i)

    def setup_ui(self):
        self.setContentsMargins(16, 16, 16, 16)
        
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        self.layout_book = QHBoxLayout()
        self.layout_main.addLayout(self.layout_book)
        self.layout_main.addSpacing(16)

        self.layout_grade = QHBoxLayout()
        self.layout_main.addLayout(self.layout_grade)
        self.layout_main.addSpacing(16)
        
        self.layout_chapter = QHBoxLayout()
        self.layout_main.addLayout(self.layout_chapter)
        self.layout_main.addSpacing(16)

        self.layout_title = QHBoxLayout()
        self.layout_main.addLayout(self.layout_title)
        self.layout_main.addSpacing(16)

        self.layout_button = QHBoxLayout()
        self.layout_main.addLayout(self.layout_button)
        
        self.label_book = QLabel("교재:")
        self.combo_book = QComboBox()
        self.combo_book.addItems(self.view_model.book_list)
        self.combo_book.currentIndexChanged.connect(self.view_model.on_book_change)
        self.layout_book.addWidget(self.label_book)
        self.layout_book.addWidget(self.combo_book)

        self.label_grade = QLabel("학년:")
        self.combo_grade = QComboBox()
        items_grade = [ of_grade(i) for i in self.view_model.grade_list ]
        self.combo_grade.addItems(items_grade)
        self.combo_grade.currentIndexChanged.connect(self.view_model.on_grade_change)
        self.layout_grade.addWidget(self.label_grade)
        self.layout_grade.addWidget(self.combo_grade)

        self.label_chapter = QLabel("단원:")
        self.combo_chapter = QComboBox()
        self.combo_chapter.currentIndexChanged.connect(self.view_model.on_chapter_change)
        self.layout_chapter.addWidget(self.label_chapter)
        self.layout_chapter.addWidget(self.combo_chapter)

        self.label_title = QLabel("번호:")
        self.edit_title = QLineEdit()
        self.edit_title.textChanged.connect(self.view_model.on_title_change)
        self.layout_title.addWidget(self.label_title)
        self.layout_title.addWidget(self.edit_title)

        self.button_submit = QPushButton('입력')
        self.button_submit.clicked.connect(self.accept)
        self.layout_button.addWidget(self.button_submit)

        self.button_cancel = QPushButton('취소')
        self.button_cancel.clicked.connect(self.reject)
        self.layout_button.addWidget(self.button_cancel)

    def get_problem_header(self) -> Student:
        if self.view_model.is_input_valid.value is False:
            return None
        grade = self.view_model.current_grade.value
        chapter = self.view_model.current_chapter.value
        book = self.view_model.current_book.value
        title = self.view_model.current_title.value
        return ProblemHeader(grade, chapter, book, title)