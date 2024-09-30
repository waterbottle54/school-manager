from datetime import datetime

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView, QTableWidget, QWidget

from ui.AddProblemFragment import *
from ui.common.Fragment import *
from ui.common.Navigation import *
from ui.common.UiUtils import *
from ui.dialogs.PromptProblemHeaderDialog import *
from ui.MissViewModel import *


class MissFragment(Fragment):

    view_model: MissViewModel

    def __init__(self, title):
        super().__init__(title)

        self.view_model = MissViewModel()

        uic.loadUi("forms/Miss.ui", self)
        self.setup_table()

        self.buttonAddMiss.clicked.connect(self.view_model.on_add_miss_click)

        self.view_model.miss_list.observe(self.update_miss_table)

        self.view_model.event.connect(self.on_event)

    def on_start(self, argument: dict):
        self.view_model.on_start(argument)
        student: Student = argument["student"]
        self.title += f" ({student.name})"

    def on_restart(self, result: dict):
        self.view_model.on_result(result)

    def on_event(self, event: MissViewModel.Event):
        if isinstance(event, MissViewModel.PromptProblemHeader):
            dialog = PromptProblemHeaderDialog(event.student.grade, None, None)
            if dialog.exec_() == QDialog.Accepted:
                problem_header = dialog.get_problem_header()
                self.view_model.on_problem_header_result(problem_header)
        if isinstance(event, MissViewModel.NavigationToAddProblemScreen):
            Navigation._instance.navigate(
                AddProblemFragment, {"problem_header": event.problem_header}
            )

    def update_miss_table(self, miss_list: list):
        self.tableMiss.setRowCount(len(miss_list))
        for i, miss in enumerate(miss_list):
            miss: Miss
            created = datetime.fromtimestamp(miss.created).strftime("%m.%d")
            updated = datetime.fromtimestamp(miss.updated).strftime("%m.%d")
            self.tableMiss.setItem(i, 0, table_item_center(created))
            self.tableMiss.setItem(i, 1, table_item_center(updated))
            self.tableMiss.setItem(i, 2, table_item_center(miss.problem_header.chapter))
            self.tableMiss.setItem(i, 3, table_item_center(miss.problem_header.book))
            self.tableMiss.setItem(i, 4, table_item_center(miss.problem_header.title))
            self.tableMiss.setItem(i, 5, table_item_center(miss.record))
            self.tableMiss.setItem(i, 6, table_item_center("-"))  # TODO: display correct answer

    def setup_table(self):
        tableWidth = self.tableMiss.width()
        self.tableMiss.setColumnWidth(0, int(tableWidth * 1 / 11))
        self.tableMiss.setColumnWidth(1, int(tableWidth * 1 / 11))
        self.tableMiss.setColumnWidth(2, int(tableWidth * 3 / 11))
        self.tableMiss.setColumnWidth(3, int(tableWidth * 2 / 11))
        self.tableMiss.setColumnWidth(4, int(tableWidth * 1 / 11))
        self.tableMiss.setColumnWidth(5, int(tableWidth * 2 / 11))
        self.tableMiss.setColumnWidth(6, int(tableWidth * 1 / 11))
