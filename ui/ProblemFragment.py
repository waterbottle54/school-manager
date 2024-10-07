from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QButtonGroup,
    QComboBox,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QVBoxLayout,
)

from common.StringRes import *
from ui.AddProblemFragment import *
from ui.common import UiUtils
from ui.common.Fragment import *
from ui.common.NonClickableCheckBox import *
from ui.common.UiUtils import *
from ui.dialogs.PromptProblemHeaderDialog import *
from ui.ProblemViewModel import *


class ProblemFragment(Fragment):

    def __init__(self, title):
        super().__init__(title)

        self.view_model = ProblemViewModel()
        
        self.layout_top = QHBoxLayout()
        self.layout_problem_list = self.setup_problem_list_layout()
        self.layout_problem_detail = self.setup_problem_detail_layout()

        self.setLayout(self.layout_top)
        self.layout_top.addLayout(self.layout_problem_list)
        self.layout_top.addStretch(1)
        self.layout_top.addLayout(self.layout_problem_detail)

        self.view_model.grade_list().observe(self.update_grade_combo)
        self.view_model.chapter_list().observe(self.update_chapter_combo)
        self.view_model.problem_list().observe(self.update_problem_table)
        self.view_model.problem_selected().observe(self.update_problem_detail)

        self.view_model.book_index().observe(self.cb_book.setCurrentIndex)
        self.view_model.grade_index().observe(self.cb_grade.setCurrentIndex)
        self.view_model.chapter_index().observe(self.cb_chapter.setCurrentIndex)
        self.view_model.problem_index().observe(self.tw_problem.selectRow)

        self.view_model.image_main.observe(
            lambda data: UiUtils.set_label_image(self.label_image_main, data)
        )
        self.view_model.image_sub.observe(
            lambda data: UiUtils.set_label_image(self.label_image_sub, data)
        )

        self.view_model.can_delete_problem.observe(self.btn_delete_problem.setEnabled)
        self.view_model.can_modify_problem.observe(self.btn_modify_problem.setEnabled)

        self.view_model.event.connect(self.on_event)

    def on_start(self, arguments: dict[str, object] | None = None):
        self.view_model.on_start()

    def on_restart(self, result: dict | None = None):
        if result is not None:
            self.view_model.on_restart(result["problem"])

    def on_event(self, event: ProblemViewModel.Event):
        if isinstance(event, ProblemViewModel.NavigateToAddProblem):
            arguments = {"problem_header": event.problem_header}
            Navigation.get_instance().navigate(AddProblemFragment, arguments)
        elif isinstance(event, ProblemViewModel.PromptProblemHeader):
            dialog = PromptProblemHeaderDialog(event.grade, event.chapter, event.book)
            if dialog.exec_() == QDialog.Accepted:
                problem_header = dialog.get_problem_header()
                self.view_model.on_problem_header_result(problem_header)
        elif isinstance(event, ProblemViewModel.ShowGeneralMessage):
            mb = QMessageBox(self)
            mb.setWindowTitle("메시지")
            mb.setText(event.message)
            mb.show()
        elif isinstance(event, ProblemViewModel.ConfirmDeleteProblem):
            mb = QMessageBox(self)
            mb.setWindowTitle("문제 삭제")
            mb.setText(f"{event.problem.title} 문제를 삭제하시겠습니까?")
            mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            mb.setDefaultButton(QMessageBox.Cancel)
            if mb.exec_() == QMessageBox.Ok:
                self.view_model.on_delete_problem_confirmed(event.problem)

    def update_grade_combo(self, g_list: list[int]):
        items = [grade_name(g) for g in g_list]
        self.cb_grade.addItems(items)

    def update_chapter_combo(self, chapters):
        self.cb_chapter.clear()
        self.cb_chapter.addItems(chapters)

    def update_problem_detail(self, problem: Problem | None):
        if problem is not None:
            self.stacked_widget.setCurrentIndex(0 if len(problem.ans_mcq) > 0 else 1)
            # mcq
            for i, button_choice in enumerate(self.list_button_choice):
                button_choice.setVisible(i < problem.num_choice)
                button_choice.setChecked(i in problem.ans_mcq)
        else:
            self.stacked_widget.setCurrentIndex(2)

    def update_problem_table(self, problem_list):
        self.tw_problem.setRowCount(len(problem_list))
        for i, problem in enumerate(problem_list):
            problem: Problem
            self.tw_problem.setItem(i, 0, table_item_center(grade_name(problem.grade)))
            self.tw_problem.setItem(i, 1, table_item_center(problem.chapter))
            self.tw_problem.setItem(i, 2, table_item_center(problem.book))
            self.tw_problem.setItem(i, 3, table_item_center(problem.title))

    def setup_problem_list_layout(self):

        layout = QVBoxLayout()

        self.layout_combos = QHBoxLayout()
        layout.addLayout(self.layout_combos)

        self.tw_problem = self.create_problem_table()
        layout.addWidget(self.tw_problem)

        self.layout_buttons = QHBoxLayout()
        layout.addLayout(self.layout_buttons)

        # combo boxes
        self.cb_book = QComboBox()
        self.layout_combos.addWidget(self.cb_book)
        self.cb_book.currentIndexChanged.connect(self.view_model.on_book_change)

        self.cb_grade = QComboBox()
        self.layout_combos.addWidget(self.cb_grade)
        self.cb_grade.currentIndexChanged.connect(self.view_model.on_grade_change)

        self.cb_chapter = QComboBox()
        self.layout_combos.addWidget(self.cb_chapter)
        self.cb_chapter.currentIndexChanged.connect(self.view_model.on_chapter_change)

        # buttons
        self.button_add_problem = QPushButton("문제 등록")
        self.button_add_problem.setObjectName("modify")
        self.button_add_problem.clicked.connect(self.view_model.on_add_problem_click)

        self.btn_modify_problem = QPushButton("수정")
        self.btn_modify_problem.setObjectName("modify")
        self.btn_modify_problem.clicked.connect(self.view_model.on_modify_problem_click)

        self.btn_delete_problem = QPushButton("삭제")
        self.btn_delete_problem.setObjectName("modify")
        self.btn_delete_problem.clicked.connect(self.view_model.on_delete_problem_click)

        self.layout_buttons.addWidget(self.button_add_problem)
        self.layout_buttons.addWidget(self.btn_modify_problem)
        self.layout_buttons.addWidget(self.btn_delete_problem)

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
        self.label_image_main.setObjectName("picture")
        self.label_image_main.setFixedSize(330, 420)
        self.label_image_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_problem_images.addWidget(self.label_image_main)

        self.layout_problem_images.addSpacing(8)

        self.label_image_sub = QLabel()
        self.label_image_sub.setObjectName("picture")
        self.label_image_sub.setFixedSize(330, 420)
        self.label_image_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        self.list_button_choice = [
            NonClickableCheckBox(f"{i+1}") for i in range(max_num_choice)
        ]
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
        verticalHeader = tw.verticalHeader()
        if verticalHeader is not None:
            verticalHeader.setVisible(False)
        tw.setHorizontalHeaderLabels(["학년", "단원", "교재", "문제"])

        tw.cellClicked.connect(self.view_model.on_problem_click)
        return tw
