from PyQt5.QtWidgets import QFrame, QSizePolicy
from abc import abstractmethod


class Fragment(QFrame):

    def __init__(self, title: str):
        super().__init__()
        self.title: str = title
        self.setContentsMargins(16, 16, 16, 16)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    @abstractmethod
    def on_start(self, arguments: dict[str, object] | None = None):
        pass

    @abstractmethod
    def on_pause(self):
        pass

    @abstractmethod
    def on_restart(self, result: dict[str, object] | None = None):
        pass

    @abstractmethod
    def on_resume(self):
        pass
