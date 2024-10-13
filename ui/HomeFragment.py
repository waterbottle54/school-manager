from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QLabel, QLineEdit, QVBoxLayout

from ui.AdminFragment import *
from ui.common.Fragment import *
from ui.HomeViewModel import *


class HomeFragment(Fragment):

    def __init__(self, title):
        super().__init__(title)

        self.name_edit = QLineEdit()

        self.view_model = HomeViewModel()
        self.setup_ui()
        self.view_model.event.connect(self.on_event)

    def on_resume(self):
        super().on_resume()
        self.name_edit: QLineEdit
        self.name_edit.setText("")
        self.name_edit.setFocus()

    def on_event(self, event):
        if isinstance(event, HomeViewModel.NavigateToAdminScreen):
            Navigation.get_instance().navigate(AdminFragment)

    def paintEvent(self, event):
        p = QPainter(self)
        p.drawPixmap(0, 0, QPixmap("images/cosmos.jpg"))

    def setup_ui(self):
        self.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        label_name = self.create_name_label()
        layout.addStretch()
        layout.addWidget(label_name)
        layout.addWidget(self.name_edit)
        layout.addStretch()

        layout.addSpacing(8)

        self.name_edit.setFixedSize(190, 50)
        self.name_edit.textChanged.connect(self.view_model.on_name_change)

    def create_name_label(self) -> QLabel:
        label = QLabel("이름을 입력해주세요")
        label.setStyleSheet("color: white; font-size: 24px;")
        shadow = QGraphicsDropShadowEffect(label)
        shadow.setColor(Qt.GlobalColor.black)
        shadow.setOffset(2, 2)
        shadow.setBlurRadius(5)
        label.setGraphicsEffect(shadow)
        return label
