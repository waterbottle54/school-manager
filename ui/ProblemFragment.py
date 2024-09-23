from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QMessageBox, QAbstractItemView)
from PyQt5.QtCore import Qt
from ui.common.Fragment import *
from ui.common.UiUtils import *
from common.StringRes import *
from ui.ProblemViewModel import *
from ui.dialogs.PromptProblemHeaderDialog import *

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
        self.view_model.current_problem_index.observe(lambda i: self.tw_problem.selectRow(i))
        self.view_model.chapter_list.observe(self.update_chapter_combo)
        self.view_model.problem_list.observe(self.update_problem_table)
        self.view_model.can_delete_problem.observe(self.button_delete_problem.setEnabled)

        self.view_model.event.connect(self.on_event)

    def on_resume(self):
        self.view_model.on_resume()

    def on_event(self, event: ProblemViewModel.Event):
        if isinstance(event, ProblemViewModel.PromptProblemHeader):
            dialog = PromptProblemHeaderDialog(event.grade, event.chapter, event.book)
            if dialog.exec_() == QDialog.Accepted:
                problem_header = dialog.get_problem_header()
                self.view_model.on_problem_header_result(problem_header)
        elif isinstance(event, ProblemViewModel.ShowGeneralMessage):
            mb = QMessageBox(self)
            mb.setWindowTitle('메시지')
            mb.setText(event.message)
            mb.show()
        elif isinstance(event, ProblemViewModel.ConfirmDeleteProblem):
            mb = QMessageBox(self)
            mb.setWindowTitle('문제 삭제')
            mb.setText(f'{event.problem.title} 문제를 삭제하시겠습니까?')
            mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            mb.setDefaultButton(QMessageBox.Cancel)
            if mb.exec_() == QMessageBox.Ok:
                self.view_model.on_delete_probem_confirmed(event.problem)

    def update_chapter_combo(self, chapters):
        self.combo_chapter.clear()
        self.combo_chapter.addItems(chapters)

    def update_chapter_combo_selection(self, i):
        self.combo_chapter.setCurrentIndex(i)

    def update_problem_table(self, problem_list):
        self.tw_problem.setRowCount(len(problem_list))
        for i, problem in enumerate(problem_list):
            problem: Problem
            self.tw_problem.setItem(i, 0, self.table_item_center(of_grade(problem.grade)))
            self.tw_problem.setItem(i, 1, self.table_item_center(problem.chapter))
            self.tw_problem.setItem(i, 2, self.table_item_center(problem.book))
            self.tw_problem.setItem(i, 3, self.table_item_center(problem.title))
    
    def table_item_center(self, text: str) -> QTableWidgetItem:
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        return item    

    def setup_problem_list_sector(self):
        self.layout_combos = QHBoxLayout()
        self.layout_left.addLayout(self.layout_combos)

        self.tw_problem = QTableWidget()
        self.tw_problem.setColumnCount(4)
        self.tw_problem.setColumnWidth(0, 50)
        self.tw_problem.setColumnWidth(1, 150)
        self.tw_problem.setColumnWidth(2, 100)
        self.tw_problem.setColumnWidth(3, 100)
        self.tw_problem.setFixedWidth(405)

        self.tw_problem.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tw_problem.setSelectionMode(QTableWidget.SingleSelection)
        self.tw_problem.setSelectionBehavior(QTableWidget.SelectRows)
        self.tw_problem.verticalHeader().setVisible(False)
        self.tw_problem.setHorizontalHeaderLabels(["학년", "단원", "교재", "문제"])
        
        self.tw_problem.cellClicked.connect(self.view_model.on_problem_click)

        self.layout_left.addWidget(self.tw_problem)

        self.layout_buttons = QHBoxLayout()
        self.layout_left.addLayout(self.layout_buttons)

        # combo boxes
        self.combo_book = QComboBox()
        self.layout_combos.addWidget(self.combo_book)
        self.combo_book.addItems(self.view_model.book_list)
        self.combo_book.currentIndexChanged.connect(self.view_model.on_book_change)

        self.combo_grade = QComboBox()
        self.layout_combos.addWidget(self.combo_grade)

        items_grade = [ of_grade(i) for i in self.view_model.grade_list ]
        self.combo_grade.addItems(items_grade)
        self.combo_grade.currentIndexChanged.connect(self.view_model.on_grade_change)
        
        self.combo_chapter = QComboBox()
        self.layout_combos.addWidget(self.combo_chapter)
        self.combo_chapter.currentIndexChanged.connect(self.view_model.on_chapter_change)

        # buttons
        self.button_add_problem = QPushButton('문제 등록')
        self.button_add_problem.setObjectName('modify')
        self.button_add_problem.clicked.connect(self.view_model.on_add_problem_click)

        self.button_delete_problem = QPushButton('문제 삭제')
        self.button_delete_problem.setObjectName('modify')
        self.button_delete_problem.clicked.connect(self.view_model.on_delete_problem_click)

        self.layout_buttons.addWidget(self.button_add_problem)
        self.layout_buttons.addWidget(self.button_delete_problem)

    def setup_problem_input_sector(self):
        empty_table = QTableWidget()
        self.layout_right.addWidget(empty_table)
