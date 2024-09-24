from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QMessageBox, QAbstractItemView, 
                             QStackedWidget, QButtonGroup, QCheckBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from ui.common.Fragment import *
from ui.AddProblemFragment import *
from ui.common.UiUtils import *
from common.StringRes import *
from ui.ProblemViewModel import *
from ui.dialogs.PromptProblemHeaderDialog import *
from ui.common.NonClickableCheckBox import *

class ProblemFragment(Fragment):

    view_model: ProblemViewModel

    layout: QHBoxLayout
   
    def __init__(self, title):
        super().__init__(title)

        self.view_model = ProblemViewModel()
        
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.layout_problem_list = self.setup_problem_list_layout()
        self.layout.addLayout(self.layout_problem_list)

        self.layout.addStretch(1)

        self.layout_problem_detail = self.setup_problem_detail_layout()
        self.layout.addLayout(self.layout_problem_detail)

        self.view_model.current_book_index.observe(self.combo_book.setCurrentIndex)
        self.view_model.current_grade_index.observe(self.combo_grade.setCurrentIndex)
        self.view_model.current_chapter_index.observe(self.combo_chapter.setCurrentIndex)
        self.view_model.current_problem_index.observe(lambda i: self.tw_problem.selectRow(i))
        self.view_model.chapter_list.observe(self.update_chapter_combo)
        self.view_model.problem_list.observe(self.update_problem_table)
        self.view_model.can_delete_problem.observe(self.button_delete_problem.setEnabled)
        self.view_model.can_modify_problem.observe(self.button_modify_problem.setEnabled)
        self.view_model.current_problem.observe(self.update_problem_detail)
        self.view_model.image_main.observe(self.update_image_main)
        self.view_model.image_sub.observe(self.update_image_sub)

        self.view_model.event.connect(self.on_event)

    def on_resume(self):
        self.view_model.on_resume()

    def on_event(self, event: ProblemViewModel.Event):
        if isinstance(event, ProblemViewModel.NavigateToAddProblem):
            arguments = {'problem_header': event.problem_header}
            Navigation._instance.navigate(AddProblemFragment, arguments)
        elif isinstance(event, ProblemViewModel.PromptProblemHeader):
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

    def update_problem_detail(self, problem: Problem):

        if problem is not None:
            self.stacked_widget.setCurrentIndex(0 if len(problem.ans_mcq) > 0 else 1)
            # mcq
            for i, button_choice in enumerate(self.list_button_choice):
                button_choice.setVisible(i < problem.num_choice)
                button_choice.setChecked(i in problem.ans_mcq)
        else:
            self.stacked_widget.setCurrentIndex(2)

    def update_image_main(self, data: bytes):
        label = self.label_image_main
        if data is not None:
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            scaled = pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(scaled)
        else:
            self.label_image_main.clear()

    def update_image_sub(self, data: bytes):
        label = self.label_image_sub
        if data is not None:
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            scaled = pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(scaled)
        else:
            self.label_image_sub.clear()

    def update_chapter_combo(self, chapters):
        self.combo_chapter.clear()
        self.combo_chapter.addItems(chapters)

    def update_chapter_combo_selection(self, i):
        self.combo_chapter.setCurrentIndex(i)

    def update_problem_table(self, problem_list):
        self.tw_problem.setRowCount(len(problem_list))
        for i, problem in enumerate(problem_list):
            problem: Problem
            self.tw_problem.setItem(i, 0, self.table_item_center(grade_name(problem.grade)))
            self.tw_problem.setItem(i, 1, self.table_item_center(problem.chapter))
            self.tw_problem.setItem(i, 2, self.table_item_center(problem.book))
            self.tw_problem.setItem(i, 3, self.table_item_center(problem.title))
    
    def table_item_center(self, text: str) -> QTableWidgetItem:
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        return item    

    def setup_problem_list_layout(self):

        layout = QVBoxLayout()

        self.layout_combos = QHBoxLayout()
        layout.addLayout(self.layout_combos)

        self.tw_problem = self.create_problem_table()
        layout.addWidget(self.tw_problem)

        self.layout_buttons = QHBoxLayout()
        layout.addLayout(self.layout_buttons)

        # combo boxes
        self.combo_book = QComboBox()
        self.layout_combos.addWidget(self.combo_book)
        self.combo_book.addItems(self.view_model.book_list)
        self.combo_book.currentIndexChanged.connect(self.view_model.on_book_change)

        self.combo_grade = QComboBox()
        self.layout_combos.addWidget(self.combo_grade)

        items_grade = [ grade_name(i) for i in self.view_model.grade_list ]
        self.combo_grade.addItems(items_grade)
        self.combo_grade.currentIndexChanged.connect(self.view_model.on_grade_change)
        
        self.combo_chapter = QComboBox()
        self.layout_combos.addWidget(self.combo_chapter)
        self.combo_chapter.currentIndexChanged.connect(self.view_model.on_chapter_change)

        # buttons
        self.button_add_problem = QPushButton('문제 등록')
        self.button_add_problem.setObjectName('modify')
        self.button_add_problem.clicked.connect(self.view_model.on_add_problem_click)

        self.button_modify_problem = QPushButton('수정')
        self.button_modify_problem.setObjectName('modify')
        self.button_modify_problem.clicked.connect(self.view_model.on_modify_problem_click)

        self.button_delete_problem = QPushButton('삭제')
        self.button_delete_problem.setObjectName('modify')
        self.button_delete_problem.clicked.connect(self.view_model.on_delete_problem_click)

        self.layout_buttons.addWidget(self.button_add_problem)
        self.layout_buttons.addWidget(self.button_modify_problem)
        self.layout_buttons.addWidget(self.button_delete_problem)

        return layout

    def setup_problem_detail_layout(self):
        
        layout = QVBoxLayout()

        # images & contents
        self.layout_problem_contents = QVBoxLayout()
        layout.addLayout(self.layout_problem_contents)

        self.layout_problem_images = QHBoxLayout()
        self.layout_problem_contents.addLayout(self.layout_problem_images)
        self.layout_problem_contents.addSpacing(16)

        # images
        self.label_image_main = QLabel()
        self.label_image_main.setObjectName('picture')
        self.label_image_main.setFixedSize(330, 420)
        self.label_image_main.setAlignment(Qt.AlignCenter)
        self.layout_problem_images.addWidget(self.label_image_main)

        self.layout_problem_images.addSpacing(8)

        self.label_image_sub = QLabel()
        self.label_image_sub.setObjectName('picture')
        self.label_image_sub.setFixedSize(330, 420)
        self.label_image_sub.setAlignment(Qt.AlignCenter)
        self.layout_problem_images.addWidget(self.label_image_sub)

        # contents (mcq or saq)
        self.stacked_widget = QStackedWidget()
        self.layout_problem_contents.addWidget(self.stacked_widget)

        self.mcq_page = self.create_mcq_page()
        self.saq_page = self.create_saq_page()
        self.empty_page = QWidget()

        self.stacked_widget.addWidget(self.mcq_page)
        self.stacked_widget.addWidget(self.saq_page)
        self.stacked_widget.addWidget(self.empty_page)

        return layout
    
    def create_mcq_page(self):
        self.layout_choices = QHBoxLayout()
       
        self.bgroup_choice = QButtonGroup()
        self.bgroup_choice.setExclusive(False)
        max_num_choice = self.view_model.range_num_choice.stop
        self.list_button_choice = [ NonClickableCheckBox(f'{i+1}') for i in range(max_num_choice) ]
        for i, button_choice in enumerate(self.list_button_choice):
            self.layout_choices.addWidget(button_choice)
            self.bgroup_choice.addButton(button_choice, i)

        self.mcq_page = QWidget()
        self.mcq_page.setLayout(self.layout_choices)
        return self.mcq_page

    def create_saq_page(self):
        self.layout_answers = QVBoxLayout()
        self.saq_page = QWidget()
        self.saq_page.setLayout(self.layout_answers)
        return self.saq_page

    def create_problem_table(self) -> QTableWidget:
        tw = QTableWidget()
        tw.setColumnCount(4)
        tw.setColumnWidth(0, 50)
        tw.setColumnWidth(1, 200)
        tw.setColumnWidth(2, 150)
        tw.setColumnWidth(3, 100)
        tw.setFixedWidth(505)

        tw.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tw.setSelectionMode(QTableWidget.SingleSelection)
        tw.setSelectionBehavior(QTableWidget.SelectRows)
        tw.verticalHeader().setVisible(False)
        tw.setHorizontalHeaderLabels(["학년", "단원", "교재", "문제"])
        
        tw.cellClicked.connect(self.view_model.on_problem_click)
        return tw
