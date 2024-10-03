from PyQt5.QtWidgets import QFrame, QSizePolicy
from abc import abstractmethod

class Fragment(QFrame):
    
    title: str = ""
    
    def __init__(self, title: str):
        super().__init__()
        self.title = title
        
        self.setContentsMargins(16, 16, 16, 16)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    @abstractmethod
    def on_start(self, arguments: dict|None = None):
        pass

    @abstractmethod
    def on_pause(self):
        pass

    @abstractmethod
    def on_restart(self, result: dict|None = None):
        pass
    
    @abstractmethod
    def on_resume(self):
        pass
