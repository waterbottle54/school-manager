from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QListWidget,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHeaderView,
)

from common.StringRes import *
from ui.common import UiUtils
from ui.common.Fragment import *
from ui.common.Navigation import *
from ui.common.UiUtils import *
from ui.dialogs.AddStudentDialog import *
from ui.dialogs.PromptProblemHeaderDialog import *
from ui.MissFragment import *
from ui.StudentViewModel import *


class StudentFragment(Fragment):

    def __init__(self, title):
        super().__init__(title)

        self._view_model = StudentViewModel()
        self._layout_top = QHBoxLayout()
        self._layout_table_sector: QVBoxLayout
        self._layout_detail_sector: QVBoxLayout

        self.setLayout(self._layout_top)

        self._layout_table_sector = self._setup_table_sector()
        self._layout_detail_sector = self._setup_detail_sector()

        self._layout_top.addLayout(self._layout_table_sector)
        self._layout_top.addSpacing(16)
        self._layout_top.addLayout(self._layout_detail_sector)

        self._view_model.get_student_list().observe(self, self._update_student_table)
        self._view_model.get_student_index().observe(
            self,
            lambda i: QTimer.singleShot(10, lambda: self._update_student_selection(i)),
        )
        self._view_model.get_selected_student().observe(
            self, self._update_student_detail
        )
        self._view_model.can_delete_student.observe(
            self, self._btn_delete_student.setEnabled
        )

        self._view_model.event.connect(self.on_event)

    def on_resume(self):
        super().on_resume()

    def on_event(self, event: StudentViewModel.Event):
        if isinstance(event, StudentViewModel.NavigateToMissScreen):
            Navigation.get_instance().navigate(MissFragment, {"student": event.student})
        elif isinstance(event, StudentViewModel.PromptStudent):
            self._prompt_student()
        elif isinstance(event, StudentViewModel.ConfirmDeleteStudent):
            self._confirm_delete_student(event.student)

    # event procedures

    def _prompt_student(self):
        dialog = AddStudentDialog()
        if dialog.exec_() == QDialog.Accepted:
            student = dialog.get_student()
            if student is not None:
                self._view_model.on_add_student_result(student)

    def _confirm_delete_student(self, student: Student):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("학생 삭제")
        msg_box.setText(f"{student.name} 학생을 삭제하시겠습니까?")
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg_box.setIcon(QMessageBox.Question)

        result = msg_box.exec_()
        if result == QMessageBox.Ok:
            self._view_model.on_delete_student_confirm(student)

    # UI update listeners

    def _update_student_table(self, student_list: list[Student]):
        self._tw_student.setRowCount(len(student_list))
        for i, student in enumerate(student_list):
            student: Student
            self._tw_student.setItem(
                i, 0, UiUtils.table_item_center(grade_name(student.grade))
            )
            self._tw_student.setItem(i, 1, UiUtils.table_item_center(student.name))
            self._tw_student.setItem(i, 2, UiUtils.table_item_center(student.school))

    def _update_student_detail(self, student: Student | None):
        if student is not None:
            text_detail = "◎  {:^6} | {:^6} | {:^12}".format(
                student.name, grade_name(student.grade), student.school
            )
            self._label_student.setText(text_detail)
        else:
            self._label_student.setText("")

        self._btn_miss_manage.setVisible(student is not None)

    def _update_student_selection(self, row: int):
        if (row >= 0) and (row < self._tw_student.rowCount()):
            self._tw_student.selectRow(row)
            self._tw_student.setFocus()

    # initialization procedures

    def _setup_table_sector(self) -> QVBoxLayout:

        self._layout_table_sector = QVBoxLayout()

        # student table
        self._tw_student = self._create_student_table()

        # add student button
        self._btn_add_student = QPushButton("학생 등록")
        self._btn_add_student.setObjectName("modify")
        self._btn_add_student.clicked.connect(self._view_model.on_add_student_click)

        # delete student button
        self._btn_delete_student = QPushButton("학생 삭제")
        self._btn_delete_student.setObjectName("modify")
        self._btn_delete_student.clicked.connect(
            self._view_model.on_delete_student_click
        )

        # placement
        self._layout_table_sector.addWidget(self._tw_student)
        self._layout_table_sector.addWidget(self._btn_add_student)
        self._layout_table_sector.addWidget(self._btn_delete_student)

        return self._layout_table_sector

    def _setup_detail_sector(self) -> QVBoxLayout:

        self._layout_detail_sector = QVBoxLayout()

        # headline
        layout_headline = QHBoxLayout()

        # - student info label
        self._label_student = QLabel()
        self._label_student.setContentsMargins(8, 8, 8, 8)

        # - miss management button
        self._btn_miss_manage = QPushButton("오답 관리")
        self._btn_miss_manage.setFixedWidth(150)
        self._btn_miss_manage.setObjectName("modify")
        self._btn_miss_manage.clicked.connect(self._view_model.on_miss_manage_click)

        # - placemant
        layout_headline.addWidget(self._label_student)
        layout_headline.addStretch(1)
        layout_headline.addWidget(self._btn_miss_manage)

        # student detail
        self._lw_detail = QListWidget()

        # placement
        self._layout_detail_sector.addLayout(layout_headline)
        self._layout_detail_sector.addWidget(self._lw_detail)

        return self._layout_detail_sector

    def _create_student_table(self) -> QTableWidget:

        tw = QTableWidget()

        tw.setColumnCount(3)
        tw.setColumnWidth(0, 100)
        tw.setColumnWidth(1, 100)
        tw.setColumnWidth(2, 200)
        tw.setFixedWidth(405)

        tw.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tw.setSelectionMode(QTableWidget.SingleSelection)
        tw.setSelectionBehavior(QTableWidget.SelectRows)

        vertical_header = tw.verticalHeader()
        if vertical_header is not None:
            vertical_header.setVisible(False)
        else:
            tw.setHorizontalHeaderLabels(["학년", "이름", "학교"])

        tw.cellClicked.connect(self._view_model.on_student_click)
        return tw
