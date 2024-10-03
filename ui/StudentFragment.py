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
from ui.common.Fragment import *
from ui.common.Navigation import *
from ui.common.UiUtils import *
from ui.dialogs.AddStudentDialog import *
from ui.dialogs.PromptProblemHeaderDialog import *
from ui.MissFragment import *
from ui.StudentViewModel import *


class StudentFragment(Fragment):

    view_model: StudentViewModel

    layout: QHBoxLayout

    def __init__(self, title):
        super().__init__(title)

        self.view_model = StudentViewModel()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.left_layout = QVBoxLayout()
        self.layout.addLayout(self.left_layout)

        self.layout.addSpacing(16)

        self.right_layout = QVBoxLayout()
        self.layout.addLayout(self.right_layout)

        self.setup_student_table_sector()
        self.setup_student_detail_sector()

        self.view_model.student_list.observe(self.update_student_table)
        self.view_model.student_index.observe(self.update_student_selection)
        self.view_model.can_delete_student.observe(
            self.button_delete_student.setEnabled
        )
        self.view_model.current_student.observe(self.update_student_detail)

        self.view_model.event.connect(self.on_event)

    def on_start(self, arguments):
        self.view_model.on_start()

    def on_event(self, event: StudentViewModel.Event):
        if isinstance(event, StudentViewModel.NavigateToMissScreen):
            Navigation.get_instance().navigate(MissFragment, {"student": event.student})
        elif isinstance(event, StudentViewModel.PromptStudent):
            self.prompt_student()
        elif isinstance(event, StudentViewModel.ConfirmDeleteStudent):
            self.confirm_delete_student(event.student)

    def update_student_table(self, student_list):
        self.tw_student.setRowCount(len(student_list))
        for i, student in enumerate(student_list):
            student: Student
            self.tw_student.setItem(
                i, 0, self.table_item_center(grade_name(student.grade))
            )
            self.tw_student.setItem(i, 1, self.table_item_center(student.name))
            self.tw_student.setItem(i, 2, self.table_item_center(student.school))

    def update_student_detail(self, student: Student):
        if student is not None:
            text_detail = "◎  {:^6} | {:^6} | {:^12}".format(
                student.name, grade_name(student.grade), student.school
            )
            self.label_student.setText(text_detail)
        else:
            self.label_student.setText("")

        self.button_miss_manage.setVisible(student is not None)

    def table_item_center(self, text: str):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return item

    def update_student_selection(self, row):
        if row >= 0 and row < self.tw_student.rowCount():
            self.tw_student.selectRow(row)
            self.tw_student.setFocus()

    def setup_student_table_sector(self):
        self.tw_student = QTableWidget()
        self.left_layout.addWidget(self.tw_student)

        self.tw_student.setColumnCount(3)
        self.tw_student.setColumnWidth(0, 100)
        self.tw_student.setColumnWidth(1, 100)
        self.tw_student.setColumnWidth(2, 200)
        self.tw_student.setFixedWidth(405)

        self.tw_student.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tw_student.setSelectionMode(QTableWidget.SingleSelection)
        self.tw_student.setSelectionBehavior(QTableWidget.SelectRows)
        vertical_header: QHeaderView = self.tw_student.verticalHeader()
        if vertical_header is not None:
            vertical_header.setVisible(False)
        self.tw_student.setHorizontalHeaderLabels(["학년", "이름", "학교"])

        self.tw_student.cellClicked.connect(self.view_model.on_student_click)

        # buttons
        self.button_add_student = QPushButton("학생 등록")
        self.button_add_student.setObjectName("modify")
        self.button_add_student.clicked.connect(self.view_model.on_add_student_click)

        self.button_delete_student = QPushButton("학생 삭제")
        self.button_delete_student.setObjectName("modify")
        self.button_delete_student.clicked.connect(
            self.view_model.on_delete_student_click
        )

        self.left_layout.addWidget(self.button_add_student)
        self.left_layout.addWidget(self.button_delete_student)

    def setup_student_detail_sector(self):

        self.right_header_layout = QHBoxLayout()
        self.right_layout.addLayout(self.right_header_layout)

        self.label_student = QLabel()
        self.label_student.setContentsMargins(8, 8, 8, 8)
        self.right_header_layout.addWidget(self.label_student)

        self.right_header_layout.addStretch(1)

        self.button_miss_manage = QPushButton("오답 관리")
        self.button_miss_manage.setFixedWidth(150)
        self.button_miss_manage.setObjectName("modify")
        self.button_miss_manage.clicked.connect(self.view_model.on_miss_manage_click)

        self.right_header_layout.addWidget(self.button_miss_manage)

        self.lw_detail = QListWidget()
        self.right_layout.addWidget(self.lw_detail)

    def prompt_student(self):
        dialog = AddStudentDialog()
        if dialog.exec_() == QDialog.Accepted:
            student = dialog.get_student()
            if student is not None:
                self.view_model.on_add_student_result(student)

    def confirm_delete_student(self, student: Student):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("학생 삭제")
        msg_box.setText(f"{student.name} 학생을 삭제하시겠습니까?")
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg_box.setIcon(QMessageBox.Question)

        result = msg_box.exec_()
        if result == QMessageBox.Ok:
            self.view_model.on_delete_student_confirm(student)
