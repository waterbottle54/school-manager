from PyQt5.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QSizePolicy, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt
from ui.common.Fragment import *
from ui.HomeViewModel import *
from ui.AdminFragment import *

class HomeFragment(Fragment):

    view_model: HomeViewModel

    def __init__(self, title):
        super().__init__(title)
        
        self.view_model = HomeViewModel()
        
        self.setup_ui()

        self.view_model.event.connect(self.on_event)

    def on_resume(self):
        self.name_edit: QLineEdit
        self.name_edit.setText("")
        self.name_edit.setFocus()

    def on_event(self, event):
        if isinstance(event, HomeViewModel.NavigateToAdminScreen):
            Navigation._instance.navigate(AdminFragment)

    def paintEvent(self, event):
        p = QPainter(self)
        p.drawPixmap(0, 0, QPixmap("images/cosmos.jpg"))

    def setup_ui(self):
        self.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout)

        label = QLabel('이름을 입력해주세요')
        label.setStyleSheet('color: white; font-size: 24px;')
        shadow = QGraphicsDropShadowEffect(label)
        shadow.setColor(Qt.GlobalColor.black)
        shadow.setOffset(2, 2)
        shadow.setBlurRadius(5)
        label.setGraphicsEffect(shadow)
        layout.addStretch()
        layout.addWidget(label)

        layout.addSpacing(8)

        self.name_edit = QLineEdit()
        self.name_edit.setFixedSize(190, 50)
        self.name_edit.textChanged.connect(self.view_model.on_name_change)
        layout.addWidget(self.name_edit)
        layout.addStretch()
