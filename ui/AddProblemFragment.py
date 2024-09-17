from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QComboBox)
from PyQt5.QtCore import Qt
from ui.common.Fragment import *
from ui.common.UiUtils import *
from common.StringRes import *
from ui.ProblemViewModel import *

class ProblemFragment(Fragment):

    view_model: ProblemViewModel

    layout: QHBoxLayout
   
    def __init__(self, title, view_model):
        super().__init__(title)

        self.view_model = view_model
        
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.layout_left = QVBoxLayout()
        self.layout.addLayout(self.layout_left)

        self.layout.addSpacing(16)

        self.layout_right = QVBoxLayout()
        self.layout.addLayout(self.layout_right)

        self.setup_problem_list_sector()
        self.setup_problem_input_sector()

        self.view_model.current_book_index.observe(self.combo_book.setCurrentIndex)
        self.view_model.current_grade_index.observe(self.combo_grade.setCurrentIndex)
        self.view_model.current_chapter_index.observe(self.combo_chapter.setCurrentIndex)
        self.view_model.chapter_list.observe(self.update_chapter_combo)

        self.view_model.event.connect(self.on_event)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.view_model.event.connect(self.on_event)

    def on_resume(self):
        self.view_model.on_resume()

    def update_chapter_combo(self, chapters):
        self.combo_chapter.clear()
        self.combo_chapter.addItems(chapters)

    def update_chapter_combo_selection(self, i):
        self.combo_chapter.setCurrentIndex(i)

    def setup_problem_list_sector(self):
        self.layout_combo = QHBoxLayout()
        self.layout_left.addLayout(self.layout_combo)

        self.combo_book = QComboBox()
        self.layout_combo.addWidget(self.combo_book)
        self.combo_book.addItems(self.view_model.book_list)
        self.combo_book.currentIndexChanged.connect(lambda index: self.view_model.on_book_change(index))

        self.combo_grade = QComboBox()
        self.layout_combo.addWidget(self.combo_grade)

        items_grade = [ of_grade(i) for i in self.view_model.grade_list ]
        self.combo_grade.addItems(items_grade)
        self.combo_grade.currentIndexChanged.connect(lambda index: self.view_model.on_grade_change(index))
        
        self.combo_chapter = QComboBox()
        self.layout_combo.addWidget(self.combo_chapter)
        self.combo_chapter.currentIndexChanged.connect(lambda index: self.view_model.on_chapter_change(index))

        self.problem_table = QTableWidget()
        self.layout_left.addWidget(self.problem_table)

    def setup_problem_input_sector(self):
        empty_table = QTableWidget()
        self.layout_right.addWidget(empty_table)
