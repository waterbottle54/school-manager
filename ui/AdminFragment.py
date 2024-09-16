from PyQt5.QtWidgets import QSizePolicy, QPushButton, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from ui.common.Fragment import *
from ui.AdminViewModel import *

class AdminFragment(Fragment):

    view_model: AdminViewModel


    def __init__(self, title, view_model):
        super().__init__(title)

        self.view_model = view_model
        
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

        button_student.setIcon(QIcon('images/student.png'))
        button_student.setIconSize(QSize(300, 300))
        button_student.clicked.connect(self.view_model.on_student_click)

        button_problem.setIcon(QIcon('images/document.png'))
        button_problem.setIconSize(QSize(256, 256))

        button_data.setIcon(QIcon('images/db.png'))
        button_data.setIconSize(QSize(256, 256))
        button_data.clicked.connect(self.view_model.on_data_click)

        button_back.setIcon(QIcon('images/back.png'))
        button_back.setIconSize(QSize(192, 192))
        button_back.clicked.connect(self.view_model.on_back_click)

        layout_buttons.addWidget(button_student, 0, 0)
        layout_buttons.addWidget(button_problem, 0, 1)
        layout_buttons.addWidget(button_data, 1, 0)
        layout_buttons.addWidget(button_back, 1, 1)

