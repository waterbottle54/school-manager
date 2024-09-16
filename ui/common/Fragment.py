from PyQt5.QtWidgets import QWidget, QSizePolicy

class Fragment(QWidget):
    
    title: str = ""

    def __init__(self, title: str):
        super().__init__()
        self.title = title

        self.setContentsMargins(16, 16, 16, 16)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def on_resume(self):
        pass