from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy


class Test:

    a: QLabel

    def __init__(self):
        self.a = QLabel()

    def fun(self):
        self.a
