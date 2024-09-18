import sys
import shutil
import os
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QFileDialog, QLabel, QSpinBox, QPushButton)
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

        self.setup_picture_section()
        self.setup_form_section()

        self.view_model.full_title.observe(self.update_title)
        self.view_model.image_path_1.observe(lambda image_path: self.update_picture(image_path, self.label_picture_1))
        self.view_model.image_path_2.observe(lambda image_path: self.update_picture(image_path, self.label_picture_2))

        self.view_model.event.connect(self.on_event)

    def update_title(self, title):
        self.title = title if title is not None else ""

    def update_picture(self, image_path, label):
        label.clear()
        if image_path is not None:
            pixmap = QPixmap(image_path)
            if pixmap is not None:
                scaled = pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                label.setPixmap(scaled)
      
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
        self.button_upload_picture_1.clicked.connect(self.view_model.on_select_picture_1_click)

        self.button_upload_picture_2 = QPushButton('사진2 업로드')
        self.button_upload_picture_2.setObjectName('modify')
        self.button_upload_picture_2.clicked.connect(self.view_model.on_select_picture_2_click)

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
