from PyQt5.QtWidgets import QFrame, QSizePolicy

class Fragment(QFrame):
    
    title: str = ""
    arguments: dict = None
    
    def __init__(self, title: str):
        super().__init__()
        self.title = title
        
        self.setContentsMargins(16, 16, 16, 16)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def on_start(self, arguments: dict = None):
        self.arguments = arguments

    def on_pause(self):
        pass

    def on_restart(self, result: dict = None):
        pass

    def on_resume(self):
        pass
