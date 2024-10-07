from PyQt5.QtCore import Qt, pyqtBoundSignal
from PyQt5.QtWidgets import QTableWidgetItem, QLabel
from PyQt5.QtGui import QPixmap


def table_item_center(text: str) -> QTableWidgetItem:
    item = QTableWidgetItem(text)
    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    return item


def disconnect(signal: pyqtBoundSignal):
    try:
        signal.disconnect()
    except:
        pass


def set_label_image(label: QLabel, data: bytes | None):
    if data is not None:
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        scaled = pixmap.scaled(
            label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        label.setPixmap(scaled)
    else:
        label.clear()
