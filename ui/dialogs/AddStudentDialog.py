from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
)
from data.SchoolRepository import *
from common.Utils import *
from data.common.LiveData import *
import numpy as np
from data.Student import *


class AddStudentDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.school = MutableLiveData("")
        self.grade = MutableLiveData(-1)
        self.name = MutableLiveData("")
        self.is_input_valid = map3(
            self.school,
            self.grade,
            self.name,
            lambda _school, _grade, _name: len(_school) > 1
            and _grade > -1
            and len(_name) > 1,
        )

        self.school_repository = SchoolRepository()
        self.school_list = self.school_repository.get_list()

        self.setWindowTitle("학생 등록")
        self.setup_ui()

        self.is_input_valid._observe(lambda valid: self.button_submit.setEnabled(valid))

    def setup_ui(self):
        self.setContentsMargins(16, 16, 16, 16)

        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        self.layout_name = QHBoxLayout()
        self.layout_main.addLayout(self.layout_name)
        self.layout_main.addSpacing(16)

        self.layout_school = QHBoxLayout()
        self.layout_main.addLayout(self.layout_school)
        self.layout_main.addSpacing(16)

        self.layout_grade = QHBoxLayout()
        self.layout_main.addLayout(self.layout_grade)
        self.layout_main.addSpacing(32)

        self.layout_button = QHBoxLayout()
        self.layout_main.addLayout(self.layout_button)

        self.label_name = QLabel("이름:")
        self.edit_name = QLineEdit()
        self.edit_name.textChanged.connect(
            lambda _name: self.name.set_value(_name.strip())
        )
        self.layout_name.addWidget(self.label_name)
        self.layout_name.addWidget(self.edit_name)

        self.label_grade = QLabel("학년:")
        self.combo_grade = QComboBox()
        self.combo_grade.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.combo_grade.currentIndexChanged.connect(self.on_grade_change)
        self.layout_grade.addWidget(self.label_grade)
        self.layout_grade.addWidget(self.combo_grade)

        self.label_school = QLabel("학교:")
        self.combo_school = QComboBox()
        self.combo_school.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.combo_school.currentIndexChanged.connect(self.on_school_change)
        self.combo_school.addItems(self.school_list)
        self.layout_school.addWidget(self.label_school)
        self.layout_school.addWidget(self.combo_school)

        self.button_submit = QPushButton("등록")
        self.button_cancel = QPushButton("취소")
        self.button_submit.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)
        self.layout_button.addWidget(self.button_submit)
        self.layout_button.addWidget(self.button_cancel)

    def on_school_change(self, index: int):
        self.combo_grade.clear()

        if index < 0 or index > len(self.school_list) - 1:
            self.school.set_value("")
            return

        self.school.set_value(self.school_list[index])

        sort = get_school_sort(self.school.value)
        end_grade = 3
        if sort is None:
            return
        if sort == SORT.ELEMENTARY:
            end_grade = 6

        self.combo_grade.addItems([f"{i}학년" for i in np.arange(1, end_grade + 1)])

    def on_grade_change(self, index: int):
        if index < 0 or index > 5:
            return

        sort = get_school_sort(self.school.value)
        if sort is None:
            return

        grade = index
        if sort == SORT.MIDDLE:
            grade += 6
        if sort == SORT.HIGH:
            grade += 9
        self.grade.set_value(grade)

    def get_student(self) -> Student | None:
        if self.is_input_valid.value is False:
            return None
        name = self.name.value
        grade = self.grade.value
        school = self.school.value
        return Student(name, grade, school)
