from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy

class Toolbar(QWidget):

    layout: QHBoxLayout
    label_title: QLabel
    button_back: QPushButton

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
        self.button_back = QPushButton('< ')
        self.button_back.setObjectName('back')
        self.button_back.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout.addWidget(self.button_back)

        self.label_title = QLabel()
        self.label_title.setObjectName('title')
        self.layout.addWidget(self.label_title)
