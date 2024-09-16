from PyQt5.QtWidgets import (QPushButton, QTableWidget, QVBoxLayout, QHBoxLayout, QMessageBox,
                             QTableWidgetItem, QAbstractItemView, QListWidget)
from PyQt5.QtCore import Qt
from ui.common.Fragment import *
from ui.StudentViewModel import *
from ui.common.UiUtils import *
from ui.AddStudentDialog import *
from common.StringRes import *

class StudentFragment(Fragment):

    view_model: StudentViewModel

    layout: QHBoxLayout
   
    def __init__(self, title, view_model):
        super().__init__(title)

        self.view_model = view_model
        
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.left_layout = QVBoxLayout()
        self.layout.addLayout(self.left_layout)

        self.layout.addSpacing(16)

        self.right_layout = QVBoxLayout()
        self.layout.addLayout(self.right_layout)

        self.setup_student_table_sector()
        self.setup_student_detail_sector()

        self.view_model.student_list.observe(self.update_student_list)
        self.view_model.student_index.observe(self.update_student_selection)
        self.view_model.can_delete_student.observe(lambda can: self.button_delete_student.setEnabled(can))
        self.view_model.current_student.observe(self.update_student_detail)

        self.view_model.event.connect(self.on_event)

    def on_resume(self):
        self.view_model.on_resume()

    def on_event(self, event: StudentViewModel.Event):
        if (isinstance(event, StudentViewModel.PromptStudent)):
            self.prompt_student()
        if (isinstance(event, StudentViewModel.ConfirmDeleteStudent)):
            self.confirm_delete_student(event.student)

    def update_student_list(self, student_list):
        self.tw_student.setRowCount(len(student_list))
        for i, student in enumerate(student_list):
            student: Student
            self.tw_student.setItem(i, 0, self.table_item_center(of_grade(student.grade)))
            self.tw_student.setItem(i, 1, self.table_item_center(student.name))
            self.tw_student.setItem(i, 2, self.table_item_center(student.school))

    def update_student_detail(self, student: Student):
        if student is not None:
            text_detail = "◎  {:^6} | {:^6} | {:^12}".format(student.name, of_grade(student.grade), student.school)
            self.label_student.setText(text_detail)
        else:
            self.label_student.setText("")

        self.button_add_wrong.setVisible(student is not None)
        self.button_remove_wrong.setVisible(student is not None)

    def table_item_center(self, text: str):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        return item

    def update_student_selection(self, row):
        if row < 0 or row >= self.tw_student.rowCount():
            pass
        self.tw_student.selectRow(row)

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

        self.tw_student.verticalHeader().setVisible(False)
        self.tw_student.setHorizontalHeaderLabels(["학년", "이름", "학교"])
        
        self.tw_student.cellClicked.connect(self.view_model.on_student_click)

        #buttons
        self.button_add_student = QPushButton('학생 등록')
        self.button_add_student.setObjectName("modify")
        self.button_add_student.clicked.connect(self.view_model.on_add_student_click)

        self.button_delete_student = QPushButton('학생 삭제')
        self.button_delete_student.setObjectName("modify")
        self.button_delete_student.clicked.connect(self.view_model.on_delete_student_click)

        self.left_layout.addWidget(self.button_add_student)
        self.left_layout.addWidget(self.button_delete_student)        

    def setup_student_detail_sector(self):

        self.right_header_layout = QHBoxLayout()
        self.right_layout.addLayout(self.right_header_layout)

        self.label_student = QLabel()
        self.label_student.setContentsMargins(8, 8, 8, 8)
        self.right_header_layout.addWidget(self.label_student)

        self.right_header_layout.addStretch(1)

        self.button_add_wrong = QPushButton('오답 추가')
        self.button_add_wrong.setFixedWidth(150)
        self.button_add_wrong.setObjectName('modify')

        self.button_remove_wrong = QPushButton('오답 제거')
        self.button_remove_wrong.setFixedWidth(150)
        self.button_remove_wrong.setObjectName('modify')

        self.right_header_layout.addWidget(self.button_add_wrong)
        self.right_header_layout.addWidget(self.button_remove_wrong)

        self.lw_wrong = QListWidget()
        self.right_layout.addWidget(self.lw_wrong)

    def prompt_student(self):
        dialog = AddStudentDialog()
        if dialog.exec_() == QDialog.Accepted:
            student = dialog.get_student()
            if student is not None:
                self.view_model.on_add_student_result(student)

    def confirm_delete_student(self, student: Student):
        msg_box = QMessageBox()
        msg_box.setWindowTitle('학생 삭제')
        msg_box.setText(f'{student.name} 학생을 삭제하시겠습니까?')
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg_box.setIcon(QMessageBox.Question)

        result = msg_box.exec_()
        if result == QMessageBox.Ok:
            self.view_model.on_delete_student_confirm(student)