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

        self._view_model = ProblemViewModel()

        self._layout_top = QHBoxLayout()
        self._layout_problem_list = self._setup_problem_list_layout()
        self._layout_problem_detail = self._setup_problem_detail_layout()

        self.setLayout(self._layout_top)
        self._layout_top.addLayout(self._layout_problem_list, stretch=1)
        self._layout_top.addSpacing(16)
        self._layout_top.addLayout(self._layout_problem_detail)

        self._view_model.book_list().observe(self, self._update_book_combo)
        self._view_model.grade_list().observe(self, self._update_grade_combo)
        self._view_model.chapter_list().observe(self, self._update_chapter_combo)
        self._view_model.problem_list().observe(self, self._update_problem_table)
        self._view_model.problem_selected().observe(self, self._update_problem_detail)

        self._view_model.book_index().observe(self, self._cb_book.setCurrentIndex)
        self._view_model.grade_index().observe(self, self._cb_grade.setCurrentIndex)
        self._view_model.chapter_index().observe(self, self._cb_chapter.setCurrentIndex)
        self._view_model.problem_index().observe(
            self,
            lambda i: QTimer.singleShot(100, lambda: self._update_problem_selection(i)),
        )

        self._view_model.image_main.observe(
            self, lambda data: UiUtils.set_label_image(self._label_image_main, data)
        )
        self._view_model.image_sub.observe(
            self, lambda data: UiUtils.set_label_image(self._label_image_sub, data)
        )

        self._view_model.can_delete_problem.observe(
            self, self._btn_delete_problem.setEnabled
        )
        self._view_model.can_modify_problem.observe(
            self, self._btn_modify_problem.setEnabled
        )

        self._view_model.event.connect(self.on_event)

    def on_resume(self):
        super().on_resume()

    def on_restart(self, result: dict[str, object] | None = None):
        if result is not None:
            problem = result["problem"]
            if isinstance(problem, Problem):
                self._view_model.on_restart(problem)

    def on_event(self, event: ProblemViewModel.Event):
        if isinstance(event, ProblemViewModel.NavigateToAddProblem):
            arguments = {"problem_header": event.problem_header}
            Navigation.get_instance().navigate(AddProblemFragment, arguments)
        elif isinstance(event, ProblemViewModel.PromptProblemHeader):
            dialog = PromptProblemHeaderDialog(event.grade, event.chapter, event.book)
            if dialog.exec_() == QDialog.Accepted:
                problem_header = dialog.get_problem_header()
                self._view_model.on_problem_header_result(problem_header)
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
                self._view_model.on_delete_problem_confirmed(event.problem)

    def _update_book_combo(self, b_list: list[str]):
        if not self._cb_book.signalsBlocked():
            self._cb_book.blockSignals(True)
            self._cb_book.clear()
            self._cb_book.addItems(b_list)
            self._cb_book.blockSignals(False)

    def _update_chapter_combo(self, c_list: list[str]):
        if not self._cb_chapter.signalsBlocked():
            self._cb_chapter.blockSignals(True)
            self._cb_chapter.clear()
            self._cb_chapter.addItems(c_list)
            self._cb_chapter.blockSignals(False)

    def _update_grade_combo(self, g_list: list[int]):
        if not self._cb_grade.signalsBlocked():
            self._cb_grade.blockSignals(True)
            items = [grade_name(g) for g in g_list]
            self._cb_grade.clear()
            self._cb_grade.addItems(items)
            self._cb_grade.blockSignals(False)

    def _update_problem_table(self, problem_list: list[Problem]):
        if not self._tw_problem.signalsBlocked():
            self._tw_problem.blockSignals(True)
            self._tw_problem.setRowCount(len(problem_list))
            for i, problem in enumerate(problem_list):
                self._tw_problem.setItem(
                    i, 0, table_item_center(grade_name(problem.grade))
                )
                self._tw_problem.setItem(i, 1, table_item_center(problem.chapter))
                self._tw_problem.setItem(i, 2, table_item_center(problem.book))
                self._tw_problem.setItem(i, 3, table_item_center(problem.title))
            self._tw_problem.blockSignals(False)

    def _update_problem_selection(self, index: int):
        if not self._tw_problem.signalsBlocked():
            self._tw_problem.blockSignals(True)
            self._tw_problem.selectRow(index)
            self._tw_problem.setFocus()
            self._tw_problem.blockSignals(False)

    def _update_problem_detail(self, problem: Problem | None):
        if problem is None:
            self._sw_problem_contents.setCurrentIndex(2)
            return
        self._sw_problem_contents.setCurrentIndex(0 if len(problem.ans_mcq) > 0 else 1)
        for i, btn_choice in enumerate(self._list_btn_choice):
            btn_choice.setVisible(i < problem.num_choice)
            btn_choice.setChecked(i in problem.ans_mcq)

    # UI initialization procedures

    def _setup_problem_list_layout(self) -> QVBoxLayout:

        layout = QVBoxLayout()

        self._layout_combos = QHBoxLayout()
        self._tw_problem = self.create_problem_table()
        self._layout_buttons = QHBoxLayout()

        layout.addLayout(self._layout_combos)
        layout.addWidget(self._tw_problem)
        layout.addLayout(self._layout_buttons)

        # combo boxes
        self._cb_book = QComboBox()
        self._cb_grade = QComboBox()
        self._cb_chapter = QComboBox()

        self._cb_book.currentIndexChanged.connect(self._view_model.on_book_change)
        self._cb_grade.currentIndexChanged.connect(self._view_model.on_grade_change)
        self._cb_chapter.currentIndexChanged.connect(self._view_model.on_chapter_change)

        self._layout_combos.addWidget(self._cb_book)
        self._layout_combos.addWidget(self._cb_grade)
        self._layout_combos.addWidget(self._cb_chapter)

        # buttons
        self._btn_add_problem = QPushButton("문제 등록")
        self._btn_modify_problem = QPushButton("수정")
        self._btn_delete_problem = QPushButton("삭제")

        self._btn_add_problem.setObjectName("modify")
        self._btn_modify_problem.setObjectName("modify")
        self._btn_delete_problem.setObjectName("modify")

        self._btn_add_problem.clicked.connect(self._view_model.on_add_problem_click)
        self._btn_modify_problem.clicked.connect(
            self._view_model.on_modify_problem_click
        )
        self._btn_delete_problem.clicked.connect(
            self._view_model.on_delete_problem_click
        )

        self._layout_buttons.addWidget(self._btn_add_problem)
        self._layout_buttons.addWidget(self._btn_modify_problem)
        self._layout_buttons.addWidget(self._btn_delete_problem)

        return layout

    def _setup_problem_detail_layout(self) -> QVBoxLayout:

        layout = QVBoxLayout()

        self._layout_problem_images = QHBoxLayout()
        layout.addLayout(self._layout_problem_images)

        # problem images sector
        self._label_image_main = QLabel()
        self._label_image_sub = QLabel()

        self._label_image_main.setObjectName("picture")
        self._label_image_sub.setObjectName("picture")

        self._label_image_main.setFixedSize(330, 420)
        self._label_image_sub.setFixedSize(330, 420)

        self._label_image_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label_image_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._layout_problem_images.addWidget(self._label_image_main)
        self._layout_problem_images.addSpacing(8)
        self._layout_problem_images.addWidget(self._label_image_sub)

        # problem contents sector (mcq or saq)
        self._sw_problem_contents = QStackedWidget()

        self._sw_problem_contents.addWidget(self.create_mcq_page())
        self._sw_problem_contents.addWidget(self.create_saq_page())
        self._sw_problem_contents.addWidget(QWidget())

        layout.addWidget(self._sw_problem_contents)

        return layout

    def create_mcq_page(self) -> QWidget:

        self._mcq_page = QWidget()
        layout = QHBoxLayout()
        self._mcq_page.setLayout(layout)

        num = self._view_model.range_num_choice.stop
        self._list_btn_choice = [NonClickableCheckBox(f"{i+1}") for i in range(num)]

        self._bgroup_choice = QButtonGroup()
        self._bgroup_choice.setExclusive(False)

        for i, btn_choice in enumerate(self._list_btn_choice):
            layout.addWidget(btn_choice)
            self._bgroup_choice.addButton(btn_choice, i)

        return self._mcq_page

    def create_saq_page(self) -> QWidget:
        self._saq_page = QWidget()
        layout = QVBoxLayout()
        self._saq_page.setLayout(layout)
        return self._saq_page

    def create_problem_table(self) -> QTableWidget:

        tw = QTableWidget()
        tw.setColumnCount(4)
        for i, width in enumerate([50, 200, 150, 100]):
            tw.setColumnWidth(i, width)

        tw.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tw.setSelectionMode(QTableWidget.SingleSelection)
        tw.setSelectionBehavior(QTableWidget.SelectRows)
        tw.cellClicked.connect(self._view_model.on_problem_click)

        tw.setHorizontalHeaderLabels(["학년", "단원", "교재", "문제"])
        verticalHeader = tw.verticalHeader()
        if verticalHeader is not None:
            verticalHeader.setVisible(False)

        return tw
