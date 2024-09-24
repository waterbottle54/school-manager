from PyQt5.QtWidgets import QWidget, QSizePolicy

class Fragment(QWidget):
    
    title: str = ""
    arguments: dict = None
    
    def __init__(self, title: str):
        super().__init__()
        self.title = title
        
        self.setContentsMargins(16, 16, 16, 16)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def set_arguments(self, arguments: dict):
        self.arguments = arguments

    def on_resume(self):
        pass
