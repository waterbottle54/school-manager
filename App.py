import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase, QKeyEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from ui.AddProblemFragment import *
from ui.AdminFragment import *
from ui.common.Navigation import *
from ui.common.Toolbar import *
from ui.DataFragment import *
from ui.HomeFragment import *
from ui.MissFragment import *
from ui.ProblemFragment import *
from ui.StudentFragment import *


class MainWindow(QMainWindow):

    navigation: Navigation
    layout: QVBoxLayout
    container: QWidget
    toolbar: Toolbar

    def __init__(self):
        super().__init__()
        self.set_stylesheet()

        self.setWindowTitle("BrainScan")
        self.setGeometry(0, 0, 1280, 740)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(self.layout)

        self.toolbar = Toolbar()
        self.layout.addWidget(self.toolbar)

        self.container = QWidget()
        self.layout.addWidget(self.container)

        self.graph = {
            HomeFragment: HomeFragment("홈"),
            AdminFragment: AdminFragment("관리자"),
            DataFragment: DataFragment("데이터 관리"),
            StudentFragment: StudentFragment("학생"),
            ProblemFragment: ProblemFragment("문제"),
            AddProblemFragment: AddProblemFragment("문제 추가"),
            MissFragment: MissFragment("오답 관리"),
        }
        self.navigation = Navigation(self.container, self.graph, HomeFragment)
        self.navigation.setup_with_toolbar(self.toolbar)
        self.navigation.set_back_stack_changed_listener(
            lambda fragment: self.toolbar.setVisible(
                not isinstance(fragment, HomeFragment)
            )
        )

        self.navigation.navigate(HomeFragment)

    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        if event is not None and event.key() == Qt.Key.Key_Escape:
            self.navigation.navigate_back()

    def set_stylesheet(self):
        with open("update_style.qss") as f:
            self.setStyleSheet(f.read())


if __name__ == "__main__":

    app = QApplication(sys.argv)
    font_id = QFontDatabase.addApplicationFont("./fonts/hakyo_R.ttf")
    app.setFont(QFont(QFontDatabase.applicationFontFamilies(font_id)[0]))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
