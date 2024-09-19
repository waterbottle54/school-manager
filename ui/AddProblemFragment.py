import sys
import shutil
import os
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QFileDialog, QLabel, QStackedWidget,
                              QPushButton, QRadioButton, QCheckBox, QButtonGroup, QComboBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from ui.common.Fragment import *
from ui.common.UiUtils import *
from common.StringRes import *
from ui.AddProblemViewModel import *
from data.ProblemHeader import *

class AddProblemFragment(Fragment):

    view_model: AddProblemViewModel
    layout: QHBoxLayout

    def __init__(self, title, view_model):
        super().__init__(title)

        self.view_model = view_model
        
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.layout_picture = self.create_picture_layout()
        self.layout.addLayout(self.layout_picture, stretch=3)

        self.layout.addSpacing(16)

        self.layout_form = self.create_form_layout()
        self.layout.addLayout(self.layout_form, stretch=2)

        self.view_model.full_title.observe(self.update_title)
        self.view_model.image_path_1.observe(lambda image_path: self.update_picture(image_path, self.label_picture_1))
        self.view_model.image_path_2.observe(lambda image_path: self.update_picture(image_path, self.label_picture_2))
        self.view_model.problem_type.observe(self.update_problem_type)
        self.view_model.current_num_choice.observe(self.update_num_choice)

        self.view_model.event.connect(self.on_event)

    def update_title(self, title):
        self.title = title if title is not None else ""

    def update_problem_type(self, type):
        self.bgroup_type.button(type).setChecked(True)
        self.stacked_widget.setCurrentIndex(type)

    def update_num_choice(self, num_choice):
        index = num_choice - self.view_model.range_num_choice.start
        self.combo_num_choice.setCurrentIndex(index)
        for i, button_choice in enumerate(self.list_button_choice):
            button_choice.setVisible(i < num_choice)
            button_choice.setChecked(False)

    def update_picture(self, image_path, label):
        label.clear()
        if image_path is not None:
            pixmap = QPixmap(image_path)
            if pixmap is not None:
                scaled = pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                label.setPixmap(scaled)
      
    def create_picture_layout(self):
        self.layout_picture = QHBoxLayout()

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
        self.button_upload_picture_1.clicked.connect(self.view_model.on_select_picture_1_click)

        self.button_upload_picture_2 = QPushButton('사진2 업로드')
        self.button_upload_picture_2.setObjectName('modify')
        self.button_upload_picture_2.clicked.connect(self.view_model.on_select_picture_2_click)

        self.layout_picture_1.addWidget(self.label_picture_1)
        self.layout_picture_1.addWidget(self.button_upload_picture_1)
        self.layout_picture_2.addWidget(self.label_picture_2)
        self.layout_picture_2.addWidget(self.button_upload_picture_2)

        return self.layout_picture

    def create_form_layout(self):
        self.layout_form = QVBoxLayout()

        # radios for problem type
        self.layout_type = QHBoxLayout()
        self.layout_form.addLayout(self.layout_type)

        self.radio_mcq = QRadioButton('객관식')
        self.radio_saq = QRadioButton('주관식')
        self.layout_type.addWidget(self.radio_mcq)
        self.layout_type.addWidget(self.radio_saq)
        
        self.bgroup_type = QButtonGroup()
        self.bgroup_type.addButton(self.radio_mcq, 0)
        self.bgroup_type.addButton(self.radio_saq, 1)
        self.bgroup_type.buttonClicked[int].connect(self.view_model.on_type_click)

        self.layout_form.addSpacing(32)

        # stacked widget to show proper page in accordance with selected problem type
        self.stacked_widget = QStackedWidget()
        self.layout_form.addWidget(self.stacked_widget)

        self.page_mcq = self.create_mcq_page()
        self.page_saq = self.create_saq_page()
        self.stacked_widget.addWidget(self.page_mcq)
        self.stacked_widget.addWidget(self.page_saq)

        # stretch
        self.layout_form.addStretch(1)

        # buttons (submit, cancel)
        self.layout_button = QHBoxLayout()
        self.layout_form.addLayout(self.layout_button)

        self.button_cancel = QPushButton('취소')
        self.button_cancel.setObjectName('modify')
        self.button_cancel.clicked.connect(self.view_model.on_cancel_click)
        self.layout_button.addWidget(self.button_cancel)

        self.button_submit = QPushButton('등록')
        self.button_submit.setObjectName('modify')
        self.button_submit.clicked.connect(self.view_model.on_submit_click)
        self.layout_button.addWidget(self.button_submit)

        return self.layout_form

    def create_mcq_page(self) -> QWidget:
        self.page_mcq = QWidget()
        self.layout_mcq = QVBoxLayout()
        self.page_mcq.setLayout(self.layout_mcq)

        self.combo_num_choice = QComboBox()
        self.combo_num_choice.setFixedWidth(200)
        self.combo_num_choice.addItems([f'{i}' for i in self.view_model.range_num_choice])
        self.combo_num_choice.activated.connect(self.view_model.on_num_choice_change)
        self.layout_mcq.addWidget(self.combo_num_choice)

        self.layout_mcq.addSpacing(16)

        self.layout_choices = QHBoxLayout()
        self.layout_mcq.addLayout(self.layout_choices)

        self.bgroup_choice = QButtonGroup()
        self.bgroup_choice.setExclusive(False)
        max_num_choice = self.view_model.range_num_choice.stop
        self.list_button_choice = [ QCheckBox(f'{i+1}') for i in range(max_num_choice) ]
        for button_choice in self.list_button_choice:
            self.layout_choices.addWidget(button_choice)
            self.bgroup_choice.addButton(button_choice)

        return self.page_mcq

    def create_saq_page(self):
        self.page_saq = QWidget()
        self.layout_saq = QVBoxLayout()
        self.page_saq.setLayout(self.layout_saq)

        return self.page_saq

    def on_resume(self):
        self.view_model.on_resume()

    def on_event(self, event):
        if isinstance(event, AddProblemViewModel.PromptImageFile):
            self.select_image(event.sequence)
        elif isinstance(event, AddProblemViewModel.MakeCopyImage):
            self.make_copy_image(event.image_path, event.folder_name, event.file_name)

    def set_problem_header(self, header: ProblemHeader):
        self.view_model.on_problem_header_set(header)

    def select_image(self, sequence):
        image_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if image_path:
            self.view_model.on_image_result(sequence, image_path)

    def make_copy_image(self, image_path, folder_name, file_name):
        os.makedirs(folder_name, exist_ok=True)
        base_name = os.path.basename(file_name)
        destination_path = os.path.join(folder_name, base_name)
        shutil.copy(image_path, destination_path)
