from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QStackedWidget,
    QVBoxLayout,
)

from common.StringRes import *
from data.ProblemHeader import *
from ui.AddProblemViewModel import *
from ui.common.Fragment import *
from ui.common.Navigation import *
from ui.common.UiUtils import *


class AddProblemFragment(Fragment):

    view_model: AddProblemViewModel
    layout: QHBoxLayout

    def __init__(self, title):
        super().__init__(title)

        self.view_model = AddProblemViewModel()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.layout_picture = self.setup_picture_layout()
        self.layout.addLayout(self.layout_picture, stretch=3)

        self.layout.addSpacing(32)

        self.layout_form = self.setup_form_layout()
        self.layout.addLayout(self.layout_form, stretch=2)

        self.view_model.problem_type.observe(self.update_problem_type)
        self.view_model.current_num_choices.observe(self.update_num_choice)
        self.view_model.answer_list_mcq.observe(self.update_choices)
        self.view_model.image_data_main.observe(
            lambda data: self.update_image(data, True)
        )
        self.view_model.image_data_sub.observe(
            lambda data: self.update_image(data, False)
        )
        self.view_model.is_input_valid.observe(self.button_submit.setEnabled)

        self.view_model.event.connect(self.on_event)
    
    def on_start(self, arguments: dict = None):
        super().on_start(arguments)
        problem_header = arguments["problem_header"]
        self.update_title(problem_header)
        self.view_model.on_start(arguments)

    def on_event(self, event):
        if isinstance(event, AddProblemViewModel.NavigateBackWithResult):
            Navigation._instance.navigate_back({"problem": event.problem})
        elif isinstance(event, AddProblemViewModel.NavigateBack):
            Navigation._instance.navigate_back()
        elif isinstance(event, AddProblemViewModel.PromptImageFile):
            self.select_image(event.is_main)
        elif isinstance(event, AddProblemViewModel.ConfirmDeleteImage):
            mb = QMessageBox(self)
            mb.setWindowTitle("이미지 삭제")
            mb.setText("이미지를 삭제하시겠습니까?")
            mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            if mb.exec_() == QMessageBox.Ok:
                self.view_model.on_delete_image_confirm(event.is_main)

    def on_choice_toggled(self, _button, _checked):
        list_chekced = []
        for i, check_button in enumerate(self.list_button_choice):
            if check_button.isChecked():
                list_chekced.append(i)
        self.view_model.on_choice_change(list_chekced)

    def select_image(self, is_main: bool):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)"
        )
        if path:
            with open(path, "rb") as file:
                self.view_model.on_image_result(file.read(), is_main)

    def update_title(self, header: ProblemHeader):
        if header is not None:
            self.title = problem_title(header)
        else:
            self.title = "-"

    def update_problem_type(self, type):
        self.bgroup_type.button(type).setChecked(True)
        self.stacked_widget.setCurrentIndex(type)

    def update_num_choice(self, num_choice):
        index = num_choice - self.view_model.range_num_choice.start
        self.combo_num_choice.setCurrentIndex(index)
        for i, button_choice in enumerate(self.list_button_choice):
            button_choice.setVisible(i < num_choice)
            button_choice.setChecked(False)

    def update_choices(self, answer_list: list):
        for i, button_choice in enumerate(self.list_button_choice):
            button_choice.setChecked(i in answer_list)

    def update_image(self, data: bytes, is_main: bool):
        label = self.label_main_image if is_main else self.label_sub_image
        button = (
            self.button_delete_main_image if is_main else self.button_delete_sub_image
        )
        button.setEnabled(data is not None)
        if data is not None:
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            scaled = pixmap.scaled(
                label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            label.setPixmap(scaled)
        else:
            label.clear()

    def setup_picture_layout(self):
        self.layout_picture = QHBoxLayout()

        self.layout_main_image = QVBoxLayout()
        self.layout_sub_image = QVBoxLayout()
        self.layout_picture.addLayout(self.layout_main_image)
        self.layout_picture.addLayout(self.layout_sub_image)

        self.label_main_image = QLabel()
        self.label_main_image.setFixedSize(350, 480)
        self.label_main_image.setObjectName("picture")

        self.label_sub_image = QLabel()
        self.label_sub_image.setFixedSize(350, 480)
        self.label_sub_image.setObjectName("picture")

        self.button_select_main_image = QPushButton("사진 업로드")
        self.button_delete_main_image = QPushButton("사진 삭제")
        self.button_select_main_image.setObjectName("modify")
        self.button_delete_main_image.setObjectName("modify")
        self.button_select_main_image.clicked.connect(
            lambda: self.view_model.on_select_image_click(True)
        )
        self.button_delete_main_image.clicked.connect(
            lambda: self.view_model.on_delete_image_click(True)
        )

        self.button_select_sub_image = QPushButton("보기 사진 업로드")
        self.button_delete_sub_image = QPushButton("보기 사진 삭제")
        self.button_select_sub_image.setObjectName("modify")
        self.button_delete_sub_image.setObjectName("modify")
        self.button_select_sub_image.clicked.connect(
            lambda: self.view_model.on_select_image_click(False)
        )
        self.button_delete_sub_image.clicked.connect(
            lambda: self.view_model.on_delete_image_click(False)
        )

        self.layout_main_image.addWidget(self.label_main_image)
        self.layout_main_image.addStretch(1)
        self.layout_main_image.addWidget(self.button_select_main_image)
        self.layout_main_image.addWidget(self.button_delete_main_image)
        self.layout_sub_image.addWidget(self.label_sub_image)
        self.layout_sub_image.addStretch(1)
        self.layout_sub_image.addWidget(self.button_select_sub_image)
        self.layout_sub_image.addWidget(self.button_delete_sub_image)

        return self.layout_picture

    def setup_form_layout(self):
        self.layout_form = QVBoxLayout()

        # radios for problem type
        self.layout_type = QHBoxLayout()
        self.layout_form.addLayout(self.layout_type)

        self.radio_mcq = QRadioButton("객관식")
        self.radio_saq = QRadioButton("주관식")
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

        self.button_cancel = QPushButton("취소")
        self.button_cancel.setObjectName("modify")
        self.button_cancel.clicked.connect(self.view_model.on_cancel_click)
        self.layout_button.addWidget(self.button_cancel)

        self.button_submit = QPushButton("등록")
        self.button_submit.setObjectName("modify")
        self.button_submit.clicked.connect(self.view_model.on_submit_click)
        self.layout_button.addWidget(self.button_submit)

        return self.layout_form

    def create_mcq_page(self) -> QWidget:
        self.page_mcq = QWidget()
        self.layout_mcq = QVBoxLayout()
        self.page_mcq.setLayout(self.layout_mcq)

        self.combo_num_choice = QComboBox()
        self.combo_num_choice.setFixedWidth(200)
        self.combo_num_choice.addItems(
            [f"{i} Choices" for i in self.view_model.range_num_choice]
        )
        self.combo_num_choice.activated.connect(self.view_model.on_num_choice_change)
        self.layout_mcq.addWidget(self.combo_num_choice)

        self.layout_mcq.addSpacing(32)

        self.layout_choices = QHBoxLayout()
        self.layout_mcq.addLayout(self.layout_choices)

        self.bgroup_choice = QButtonGroup()
        self.bgroup_choice.setExclusive(False)
        max_num_choice = self.view_model.range_num_choice.stop
        self.list_button_choice = [QCheckBox(f"{i+1}") for i in range(max_num_choice)]
        for i, button_choice in enumerate(self.list_button_choice):
            self.layout_choices.addWidget(button_choice)
            self.bgroup_choice.addButton(button_choice, i)

        self.bgroup_choice.buttonToggled.connect(self.on_choice_toggled)

        return self.page_mcq

    def create_saq_page(self):
        self.page_saq = QWidget()
        self.layout_saq = QVBoxLayout()
        self.page_saq.setLayout(self.layout_saq)

        return self.page_saq
