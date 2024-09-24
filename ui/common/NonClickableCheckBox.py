from PyQt5.QtWidgets import QCheckBox

class NonClickableCheckBox(QCheckBox):
    def mousePressEvent(self, event):
        # Override the mouse press event to do nothing
        pass  # Ignore the click