from PyQt5.QtWidgets import QLayout, QVBoxLayout
from ui.common.Fragment import *
from ui.common.Toolbar import *

class Navigation:

    container: QWidget
    
    graph: dict
    home_fragment: Fragment
    current_fragment: Fragment

    back_stack: list[Fragment]
    back_stack_changed = None

    fragment_result_interceptor: Fragment
    data_result: dict

    toolbar: Toolbar = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):         
            cls._instance = super().__new__(cls) 
        return cls._instance                    

    def __init__(self, container: QWidget, graph: dict, home):
        cls = type(self)
        if not hasattr(cls, "_init"):             
            self.container = container
            self.layout = QVBoxLayout()
            self.container.setLayout(self.layout)
            self.graph = graph
            self.home_fragment = graph[home]
            self.current_fragment = None
            self.back_stack = []
            self.data_result = {}
            self.fragment_result_interceptor = None
            cls._init = True

    def set_back_stack_changed_listener(self, listener):
        self.back_stack_changed = listener

    def setup_with_toolbar(self, toolbar: Toolbar):
        self.toolbar = toolbar
        self.toolbar.button_back.clicked.connect(self.navigate_back)

    def navigate(self, cls, arguments: dict = None):
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

    def navigate_back(self, data_result: dict = None):
        if len(self.back_stack) > 0:
            self.current_fragment.on_pause()

            self.layout.removeWidget(self.current_fragment)
            self.current_fragment.setParent(None)
            
            self.current_fragment = self.back_stack.pop()
            self.layout.addWidget(self.current_fragment)

            self.current_fragment.restart(data_result)
            self.on_fragment_change()

    def on_fragment_change(self):
        self.current_fragment.on_resume()

        if self.back_stack_changed is not None:
            self.back_stack_changed(self.current_fragment)

        self.update_toolbar()

    def update_toolbar(self):

        if self.update_toolbar is None:
            return
        
        layout = self.toolbar.layout
        label_title = self.toolbar.label_title
        button_back = self.toolbar.button_back
        
        if self.current_fragment != self.home_fragment:
            label_title.setVisible(True)
            button_back.setVisible(True)
            layout.setContentsMargins(20, 16, 20, 16)
        else:
            label_title.setVisible(False)
            button_back.setVisible(False)
            layout.setContentsMargins(0, 0, 0, 0)

        button_back.setVisible(len(self.back_stack) > 0)
        label_title.setText(self.current_fragment.title)
