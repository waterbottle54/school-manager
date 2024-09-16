from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QComboBox)
from PyQt5.QtCore import Qt
from ui.common.Fragment import *
from ui.common.UiUtils import *
from common.StringRes import *
from ui.ProblemViewModel import *

class ProblemFragment(Fragment):

    view_model: ProblemViewModel

    layout: QHBoxLayout
   
    def __init__(self, title, view_model):
        super().__init__(title)

        self.view_model = view_model
        
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.layout_left = QVBoxLayout()
        self.layout.addLayout(self.layout_left)

        self.layout.addSpacing(16)

        self.right_layout = QVBoxLayout()
        self.layout.addLayout(self.right_layout)

        self.setup_problem_list_sector()
        self.setup_problem_input_sector()

        self.view_model.event.connect(self.on_event)

    def on_resume(self):
        self.view_model.on_resume()

    def on_event(self, event: ProblemViewModel.Event):
        if (isinstance(event, ProblemViewModel.ConfirmDeleteStudent)):
            pass

    def setup_problem_list_sector(self):
        self.layout_combo = QHBoxLayout()
        self.layout_left.addLayout(self.layout_combo)

        self.combo_grade = QComboBox()
        self.layout_combo.addWidget(self.combo_grade)

    def setup_problem_input_sector(self):
        pass
