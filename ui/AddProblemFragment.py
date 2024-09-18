from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QSpinBox, QPushButton)
from PyQt5.QtCore import Qt
from ui.common.Fragment import *
from ui.common.UiUtils import *
from common.StringRes import *
from ui.AddProblemViewModel import *
from data.ProblemHeader import *

class AddProblemFragment(Fragment):

    view_model: AddProblemViewModel
    layout: QHBoxLayout

    problem_header: ProblemHeader
   
    def __init__(self, title, view_model):
        super().__init__(title)

        self.view_model = view_model
        
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.setup_picture_section()
        self.setup_form_section()

        self.view_model.event.connect(self.on_event)

    def setup_picture_section(self):
        self.layout_picture = QHBoxLayout()
        self.layout.addLayout(self.layout_picture)

        self.layout_picture_1 = QVBoxLayout()
        self.layout_picture_2 = QVBoxLayout()
        self.layout_picture.addLayout(self.layout_picture_1)
        self.layout_picture.addLayout(self.layout_picture_2)

        self.label_picture_1 = QLabel()
        self.label_picture_1.setObjectName('picture')

        self.label_picture_2 = QLabel()
        self.label_picture_2.setObjectName('picture')

        self.button_upload_picture_1 = QPushButton('사진1 업로드')
        self.button_upload_picture_1.setObjectName('modify')
        self.button_upload_picture_1.clicked.connect(self.view_model.on_upload_picture_1_click)

        self.button_upload_picture_2 = QPushButton('사진2 업로드')
        self.button_upload_picture_2.setObjectName('modify')
        self.button_upload_picture_2.clicked.connect(self.view_model.on_upload_picture_2_click)

        self.layout_picture_1.addWidget(self.label_picture_1)
        self.layout_picture_1.addWidget(self.button_upload_picture_1)
        self.layout_picture_2.addWidget(self.label_picture_2)
        self.layout_picture_2.addWidget(self.button_upload_picture_2)

    def setup_form_section(self):
        self.layout_form = QVBoxLayout()
        self.layout.addLayout(self.layout_form)

        self.spinner = QSpinBox()
        self.spinner.setRange(3, 8)
        self.spinner.setSingleStep(1)
        self.spinner.setValue(5)

        self.layout_form.addWidget(self.spinner)

    def on_resume(self):
        self.view_model.on_resume()

    def on_event(self, event):
        pass

    def set_problem_header(self, header: ProblemHeader):
        self.problem_header = header
        if header is not None:
            self.title = f"{header.book} {of_grade(header.grade)}-{header.chapter} prob.{header.title}"
