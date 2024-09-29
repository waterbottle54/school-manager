from PyQt5.QtWidgets import (QWidget, QTableWidget, QAbstractItemView)
from PyQt5.QtCore import Qt
from ui.common.Fragment import *
from ui.MissViewModel import *
from ui.dialogs.PromptProblemHeaderDialog import *
from PyQt5 import uic

class MissFragment(Fragment):

    view_model: MissViewModel

    def __init__(self, title):
        super().__init__(title)

        self.view_model = MissViewModel()

        uic.loadUi('forms/Miss.ui', self)
        self.setup_table()

        self.buttonAddMiss.clicked.connect(self.view_model.on_add_miss_click)

        self.view_model.event.connect(self.on_event)

    def on_start(self, argument: dict):
        self.view_model.on_start(argument)
        self.title += f'({argument['student']})'

    def on_restart(self, result: dict):
        self.view_model.on_result(result)

    def on_event(self, event: MissViewModel.Event):
        if isinstance(event, MissViewModel.PromptProblemHeader):
            dialog =  PromptProblemHeaderDialog(event.student.grade, None, None)
            if dialog.exec_() == QDialog.Accepted:
                problem_header = dialog.get_problem_header()
                self.view_model.on_problem_header_result(problem_header)

    def setup_table(self):
        tableWidth = self.tableMiss.width()
        self.tableMiss.setColumnWidth(0, int(tableWidth * 1/11))
        self.tableMiss.setColumnWidth(1, int(tableWidth * 1/11))
        self.tableMiss.setColumnWidth(2, int(tableWidth * 2/11))
        self.tableMiss.setColumnWidth(3, int(tableWidth * 3/11))
        self.tableMiss.setColumnWidth(4, int(tableWidth * 1/11))
        self.tableMiss.setColumnWidth(5, int(tableWidth * 2/11))
        self.tableMiss.setColumnWidth(6, int(tableWidth * 1/11))
        self.tableMiss.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableMiss.setSelectionMode(QTableWidget.SingleSelection)
        self.tableMiss.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableMiss.verticalHeader().setVisible(False)