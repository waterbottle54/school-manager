from PyQt5.QtWidgets import QVBoxLayout
from typing import Callable, Optional

from ui.common.Fragment import *
from ui.common.Toolbar import *


class Navigation:

    _instance: Optional["Navigation"] = None

    @staticmethod
    def get_instance() -> "Navigation":
        if Navigation._instance is None:
            raise Exception("Navigation singleton instance not initialized yet.")
        return Navigation._instance

    def __init__(
        self, container: QWidget, _graph: dict[type, Fragment], home: Fragment
    ):
        self.container = container
        self.layout: QVBoxLayout
        self.graph = _graph
        self.home_fragment = _graph[home]
        self.current_fragment: Fragment
        self.back_stack = list[Fragment]()
        self.back_stack_change_listener: Callable[[Fragment], None] | None = None
        self.toolbar: Toolbar | None = None
        if Navigation._instance is None:
            Navigation._instance = self

    def set_back_stack_change_listener(self, listener: Callable[[Fragment], None]):
        self.back_stack_change_listener = listener

    def setup_with_toolbar(self, toolbar: Toolbar):
        self.toolbar = toolbar
        toolbar.get_back_button().clicked.connect(self.navigate_back)

    def navigate(self, cls, arguments: dict | None = None):
        if cls not in self.graph:
            return

        if self.current_fragment is not None:
            self.back_stack.append(self.current_fragment)
            self.layout.removeWidget(self.current_fragment)
            self.current_fragment.setParent(None)

        self.current_fragment = self.graph[cls]
        self.layout.addWidget(self.current_fragment)

        self.current_fragment.on_start(arguments)
        self.on_fragment_change()

    def navigate_back(self, data_result: dict | None = None):
        if len(self.back_stack) > 0:
            self.current_fragment.on_pause()

            self.layout.removeWidget(self.current_fragment)
            self.current_fragment.setParent(None)

            self.current_fragment = self.back_stack.pop()
            self.layout.addWidget(self.current_fragment)

            self.current_fragment.on_restart(data_result)
            self.on_fragment_change()

    def on_fragment_change(self):
        self.current_fragment.on_resume()

        if self.back_stack_change_listener is not None:
            self.back_stack_change_listener(self.current_fragment)

        self.update_toolbar()

    def update_toolbar(self):
        if self.toolbar is None:
            return

        layout_toolbar = self.toolbar.get_top_layout()
        label_title = self.toolbar.get_title_label()
        button_back = self.toolbar.get_back_button()

        if self.current_fragment != self.home_fragment:
            label_title.setVisible(True)
            button_back.setVisible(True)
            layout_toolbar.setContentsMargins(20, 16, 20, 16)
        else:
            label_title.setVisible(False)
            button_back.setVisible(False)
            layout_toolbar.setContentsMargins(0, 0, 0, 0)

        button_back.setVisible(len(self.back_stack) > 0)
        label_title.setText(self.current_fragment.title)
