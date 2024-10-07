from datetime import datetime
import re

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget

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
        self._setup_miss_table()

        self.buttonAddMiss: QPushButton
        self.buttonDeleteMiss: QPushButton
        self.buttonModifyProblem: QPushButton
        self.buttonAddMiss.clicked.connect(self.view_model.on_add_miss_click)
        self.buttonDeleteMiss.clicked.connect(self.view_model.on_delete_miss_click)

        self.labelImageMain: QLabel
        self.labelImageSub: QLabel
        self.labelImageMain.setScaledContents(True)
        self.labelImageSub.setScaledContents(True)

        self.view_model.miss_list.observe(self._update_miss_table)
        self.view_model.current_miss_index.observe(self._update_miss_selection)
        self.view_model.current_miss.observe(self._update_miss_detail)
        self.view_model.can_delete_miss.observe(self.buttonDeleteMiss.setEnabled)
        self.view_model.can_modify_problem.observe(self.buttonModifyProblem.setEnabled)
        self.view_model.image_main.observe(self._update_main_image)
        self.view_model.image_sub.observe(self._update_sub_image)

        self.view_model.event.connect(self.on_event)

    def on_start(self, argument: dict):
        self.view_model.on_start(argument)
        student: Student = argument["student"]
        self.title = re.sub(r"\s*\(.*?\)", "", self.title).strip()
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
            Navigation.get_instance().navigate(
                AddProblemFragment, {"problem_header": event.problem_header}
            )
        if isinstance(event, MissViewModel.ConfirmDeleteMiss):
            self._confirm_delete_miss(event.miss)

    def _update_miss_table(self, miss_list: list):
        table: QTableWidget = self.tableMiss
        table.setRowCount(len(miss_list))
        for i, miss in enumerate(miss_list):
            miss: Miss
            created = datetime.fromtimestamp(miss.created).strftime("%m.%d")
            updated = datetime.fromtimestamp(miss.updated).strftime("%m.%d")
            table.setItem(i, 0, table_item_center(created))
            table.setItem(i, 1, table_item_center(updated))
            table.setItem(i, 2, table_item_center(miss.problem_header.chapter))
            table.setItem(i, 3, table_item_center(miss.problem_header.book))
            table.setItem(i, 4, table_item_center(miss.problem_header.title))
            table.setItem(i, 5, table_item_center(miss.record))
            table.setItem(i, 6, table_item_center("-"))  # TODO: display correct answer

    def _update_miss_selection(self, index: int):
        table: QTableWidget = self.tableMiss
        if index >= 0 and index < table.rowCount():
            table.selectRow(index)
            table.setFocus()

    def _update_miss_detail(self, miss: Miss | None):
        pass

    def _update_main_image(self, image_data: bytes | None):
        label: QLabel = self.labelImageMain
        if image_data is not None:
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            label.setPixmap(pixmap)
        else:
            label.clear()

    def _update_sub_image(self, image_data: bytes | None):
        label: QLabel = self.labelImageSub
        if image_data is not None:
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            label.setPixmap(pixmap)
        else:
            label.clear()

    def _confirm_delete_miss(self, miss: Miss):
        mb = QMessageBox()
        mb.setWindowTitle("오답 삭제")
        mb.setText(f'오답 "{miss.problem_header.title}"을 삭제하시겠습니까?')
        mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if mb.exec_() == QMessageBox.Ok:
            self.view_model.on_delete_message_confirm(miss)

    def _setup_miss_table(self):
        table: QTableWidget = self.tableMiss
        tableWidth = table.width()
        table.setColumnWidth(0, int(tableWidth * 1 / 11))
        table.setColumnWidth(1, int(tableWidth * 1 / 11))
        table.setColumnWidth(2, int(tableWidth * 3 / 11))
        table.setColumnWidth(3, int(tableWidth * 2 / 11))
        table.setColumnWidth(4, int(tableWidth * 1 / 11))
        table.setColumnWidth(5, int(tableWidth * 2 / 11))
        table.setColumnWidth(6, int(tableWidth * 1 / 11))
        table.cellClicked.connect(self.view_model.on_miss_selected)
