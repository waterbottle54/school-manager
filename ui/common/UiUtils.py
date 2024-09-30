from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem


def table_item_center(text: str) -> QTableWidgetItem:
    item = QTableWidgetItem(text)
    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    return item
