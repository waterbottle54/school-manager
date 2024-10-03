from PyQt5.QtWidgets import QSizePolicy, QPushButton, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from ui.common.Fragment import *
from ui.AdminViewModel import *
from ui.DataFragment import *
from ui.StudentFragment import *
from ui.ProblemFragment import *


class AdminFragment(Fragment):

    view_model: AdminViewModel

    def __init__(self, title):
        super().__init__(title)

        self.view_model = AdminViewModel()

        self.setup_ui()

        self.view_model.event.connect(self.on_event)

    def on_event(self, event):
        if isinstance(event, AdminViewModel.NavigateBack):
            Navigation.get_instance().navigate_back()
        elif isinstance(event, AdminViewModel.NavigateToDataFragment):
            Navigation.get_instance().navigate(DataFragment)
        elif isinstance(event, AdminViewModel.NavigateToStudentFragment):
            Navigation.get_instance().navigate(StudentFragment)
        elif isinstance(event, AdminViewModel.NavigateToProblemFragment):
            Navigation.get_instance().navigate(ProblemFragment)

    def setup_ui(self):
        layout_buttons = QGridLayout()
        self.setLayout(layout_buttons)

        button_student = QPushButton("")
        button_problem = QPushButton("")
        button_data = QPushButton("")
        button_back = QPushButton("")

        button_student.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_problem.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_data.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_back.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        button_student.setIcon(QIcon("images/student.png"))
        button_student.setIconSize(QSize(300, 300))
        button_student.clicked.connect(self.view_model.on_student_click)

        button_problem.setIcon(QIcon("images/document.png"))
        button_problem.setIconSize(QSize(256, 256))
        button_problem.clicked.connect(self.view_model.on_problem_click)

        button_data.setIcon(QIcon("images/db.png"))
        button_data.setIconSize(QSize(256, 256))
        button_data.clicked.connect(self.view_model.on_data_click)

        button_back.setIcon(QIcon("images/back.png"))
        button_back.setIconSize(QSize(192, 192))
        button_back.clicked.connect(self.view_model.on_back_click)

        layout_buttons.addWidget(button_student, 0, 0)
        layout_buttons.addWidget(button_problem, 0, 1)
        layout_buttons.addWidget(button_data, 1, 0)
        layout_buttons.addWidget(button_back, 1, 1)
