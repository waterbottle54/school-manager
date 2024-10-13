from PyQt5.QtWidgets import QFrame, QSizePolicy
from abc import abstractmethod
from typing import Callable


class Fragment(QFrame):

    def __init__(self, title: str):
        super().__init__()
        self.title: str = title
        self.setContentsMargins(16, 16, 16, 16)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._resume_observers: list[Callable[[], None]] = []

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
        for observer in self._resume_observers:
            observer()

    def observe_resume(self, observer: Callable[[], None]):
        self._resume_observers.append(observer)
