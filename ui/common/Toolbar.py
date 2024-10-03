from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy


class Toolbar(QWidget):

    def __init__(self):
        super().__init__()

        self.layout_top = QHBoxLayout()
        self.label_title = QLabel()
        self.button_back = QPushButton()

        self.layout_top.addWidget(self.button_back)
        self.layout_top.addWidget(self.label_title)

        self.button_back = QPushButton("< ")
        self.button_back.setObjectName("back")
        self.button_back.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.label_title = QLabel()
        self.label_title.setObjectName("title")

    def get_top_layout(self) -> QHBoxLayout:
        return self.layout_top

    def get_back_button(self) -> QPushButton:
        return self.button_back

    def get_title_label(self) -> QLabel:
        return self.label_title
