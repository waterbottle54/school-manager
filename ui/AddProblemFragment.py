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

    def __init__(self, title):
        super().__init__(title)

        self._view_model = AddProblemViewModel()
        self._layout_top = QHBoxLayout()
        self._layout_picture: QHBoxLayout
        self._layout_form: QVBoxLayout

        self.setLayout(self._layout_top)
        self._layout_picture = self.setup_picture_layout()
        self._layout_form = self.setup_form_layout()

        self._layout_top.addLayout(self._layout_picture, stretch=3)
        self._layout_top.addSpacing(32)
        self._layout_top.addLayout(self._layout_form, stretch=2)

        self._view_model.problem_type.observe(self, self.update_problem_type)
        self._view_model.current_num_choices.observe(self, self.update_num_choice)
        self._view_model.answer_list_mcq.observe(self, self.update_choices)
        self._view_model.image_data_main.observe(
            self, lambda data: self.update_image(data, True)
        )
        self._view_model.image_data_sub.observe(
            self, lambda data: self.update_image(data, False)
        )
        self._view_model.is_input_valid.observe(self, self._btn_submit.setEnabled)

        self._view_model._event.connect(self.on_event)

    def on_start(self, arguments: dict[str, object] | None = None):
        self._view_model.on_start(arguments)

    def on_event(self, event):
        if isinstance(event, AddProblemViewModel.NavigateBackWithResult):
            Navigation.get_instance().navigate_back({"problem_id": event.problem_id})
        elif isinstance(event, AddProblemViewModel.NavigateBack):
            Navigation.get_instance().navigate_back()
        elif isinstance(event, AddProblemViewModel.PromptImageFile):
            self.select_image(event.is_main)
        elif isinstance(event, AddProblemViewModel.ConfirmDeleteImage):
            mb = QMessageBox(self)
            mb.setWindowTitle("이미지 삭제")
            mb.setText("이미지를 삭제하시겠습니까?")
            mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            if mb.exec_() == QMessageBox.Ok:
                self._view_model.on_delete_image_confirmed(event.is_main)

    def on_choice_toggled(self, _button, _checked):
        list_chekced = []
        for i, check_button in enumerate(self.list_btn_choice):
            if check_button.isChecked():
                list_chekced.append(i)
        self._view_model.on_choice_changed(list_chekced)

    def update_title(self, header: ProblemHeader):
        self.title = problem_title(header) if (header is not None) else "-"

    def update_problem_type(self, _type):
        button_type = self._bgroup_type.button(_type)
        if button_type is not None:
            button_type.setChecked(True)
        self._stacked_widget.setCurrentIndex(_type)

    def update_num_choice(self, num_choice: int):
        index = num_choice - self._view_model.range_num_choice.start
        self.combo_num_choice.setCurrentIndex(index)
        for i, button_choice in enumerate(self.list_btn_choice):
            button_choice.setVisible(i < num_choice)
            button_choice.setChecked(False)

    def update_choices(self, answer_list: list[int]):
        for i, button_choice in enumerate(self.list_btn_choice):
            button_choice.setChecked(i in answer_list)

    def update_image(self, data: bytes | None, is_main: bool):
        label = self.label_main_image if is_main else self.label_sub_image
        button = (
            self.button_delete_main_image if is_main else self.button_delete_sub_image
        )
        button.setEnabled(data is not None)
        if data is not None:
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            scaled = pixmap.scaled(
                label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            label.setPixmap(scaled)
        else:
            label.clear()

    def select_image(self, is_main: bool):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)"
        )
        if path:
            with open(path, "rb") as file:
                self._view_model.on_image_result(file.read(), is_main)

    def setup_picture_layout(self) -> QHBoxLayout:
        self._layout_picture = QHBoxLayout()

        # main image layout
        self.layout_main_image = QVBoxLayout()

        # - image label
        self.label_main_image = QLabel()
        self.label_main_image.setFixedSize(350, 480)
        self.label_main_image.setObjectName("picture")

        # - upload image button
        self.button_select_main_image = QPushButton("사진 업로드")
        self.button_select_main_image.setObjectName("modify")
        self.button_select_main_image.clicked.connect(
            lambda: self._view_model.on_select_image_click(True)
        )

        # - delete image button
        self.button_delete_main_image = QPushButton("사진 삭제")
        self.button_delete_main_image.setObjectName("modify")
        self.button_delete_main_image.clicked.connect(
            lambda: self._view_model.on_delete_image_click(True)
        )

        # - placement of main image layout
        self.layout_main_image.addWidget(self.label_main_image)
        self.layout_main_image.addStretch(1)
        self.layout_main_image.addWidget(self.button_select_main_image)
        self.layout_main_image.addWidget(self.button_delete_main_image)

        # sub image layout
        self.layout_sub_image = QVBoxLayout()

        # - image label
        self.label_sub_image = QLabel()
        self.label_sub_image.setFixedSize(350, 480)
        self.label_sub_image.setObjectName("picture")

        # - select image button
        self.button_select_sub_image = QPushButton("보기 사진 업로드")
        self.button_select_sub_image.setObjectName("modify")
        self.button_select_sub_image.clicked.connect(
            lambda: self._view_model.on_select_image_click(False)
        )

        # - delete image button
        self.button_delete_sub_image = QPushButton("보기 사진 삭제")
        self.button_delete_sub_image.setObjectName("modify")
        self.button_delete_sub_image.clicked.connect(
            lambda: self._view_model.on_delete_image_click(False)
        )

        # - placement of sub image layout
        self.layout_sub_image.addWidget(self.label_sub_image)
        self.layout_sub_image.addStretch(1)
        self.layout_sub_image.addWidget(self.button_select_sub_image)
        self.layout_sub_image.addWidget(self.button_delete_sub_image)

        # placement
        self._layout_picture.addLayout(self.layout_main_image)
        self._layout_picture.addLayout(self.layout_sub_image)

        return self._layout_picture

    def setup_form_layout(self) -> QVBoxLayout:
        self._layout_form = QVBoxLayout()

        # radio buttons to select type of problem (MCQ, SAQ)
        self._layout_type = QHBoxLayout()
        self._radio_mcq = QRadioButton("객관식")
        self._radio_saq = QRadioButton("주관식")
        self._layout_type.addWidget(self._radio_mcq)
        self._layout_type.addWidget(self._radio_saq)

        # - button groups that manage the radio buttons
        self._bgroup_type = QButtonGroup()
        self._bgroup_type.addButton(self._radio_mcq, 0)
        self._bgroup_type.addButton(self._radio_saq, 1)
        self._bgroup_type.buttonClicked[int].connect(self._view_model.on_type_click)

        # stacked widget to switch UI type (MCQ, SAQ)
        self._stacked_widget = QStackedWidget()
        self._page_mcq = self.create_mcq_page()
        self._page_saq = self.create_saq_page()
        self._stacked_widget.addWidget(self._page_mcq)
        self._stacked_widget.addWidget(self._page_saq)

        # horizontal buttons (submit, cancel)
        self._layout_form_buttons = QHBoxLayout()

        # - cancel button
        self._btn_cancel = QPushButton("취소")
        self._btn_cancel.setObjectName("modify")
        self._btn_cancel.clicked.connect(self._view_model.on_cancel_click)

        # - submit button
        self._btn_submit = QPushButton("등록")
        self._btn_submit.setObjectName("modify")
        self._btn_submit.clicked.connect(self._view_model.on_submit_click)

        # - placement of buttons
        self._layout_form_buttons.addWidget(self._btn_cancel)
        self._layout_form_buttons.addWidget(self._btn_submit)

        # placement
        self._layout_form.addLayout(self._layout_type)
        self._layout_form.addSpacing(32)
        self._layout_form.addWidget(self._stacked_widget)
        self._layout_form.addStretch(1)
        self._layout_form.addLayout(self._layout_form_buttons)

        return self._layout_form

    def create_mcq_page(self) -> QWidget:
        self._page_mcq = QWidget()
        self.layout_mcq = QVBoxLayout()
        self._page_mcq.setLayout(self.layout_mcq)

        # combo box to select number of choices
        self.combo_num_choice = QComboBox()
        self.combo_num_choice.setFixedWidth(200)
        self.combo_num_choice.addItems(
            [f"{i} Choices" for i in self._view_model.range_num_choice]
        )
        self.combo_num_choice.activated.connect(self._view_model.on_num_choice_change)

        # horizontal check boxes to select answer
        self.layout_choices = QHBoxLayout()
        max_num_choice = self._view_model.range_num_choice.stop
        self.list_btn_choice = [QCheckBox(f"{i+1}") for i in range(max_num_choice)]

        self._bgroup_choice = QButtonGroup()
        for i, button_choice in enumerate(self.list_btn_choice):
            self._bgroup_choice.addButton(button_choice, i)
            self.layout_choices.addWidget(button_choice)

        self._bgroup_choice.buttonToggled.connect(self.on_choice_toggled)

        # placement
        self.layout_mcq.addWidget(self.combo_num_choice)
        self.layout_mcq.addSpacing(32)
        self.layout_mcq.addLayout(self.layout_choices)

        return self._page_mcq

    def create_saq_page(self) -> QWidget:
        # TODO: build SAQ UI
        self._page_saq = QWidget()
        self.layout_saq = QVBoxLayout()
        self._page_saq.setLayout(self.layout_saq)
        return self._page_saq
