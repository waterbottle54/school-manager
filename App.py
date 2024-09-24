import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QKeyEvent, QPainter, QPixmap, QFontDatabase, QFont
from PyQt5.QtCore import Qt
from ui.HomeFragment import *
from ui.AdminFragment import *
from ui.DataFragment import *
from ui.StudentFragment import *
from ui.StudentViewModel import *
from ui.ProblemFragment import *
from ui.ProblemViewModel import *
from ui.AddProblemFragment import *
from ui.AddProblemViewModel import *
from ui.common.Navigation import *
from ui.common.Toolbar import *

class MainWindow(QMainWindow):

    navigation: Navigation
    layout: QVBoxLayout
    toolbar: Toolbar

    def __init__(self):
        super().__init__()
        self.set_stylesheet()
        
        self.setWindowTitle("BrainScan")
        self.setGeometry(0, 0, 1280, 740)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)
        
        self.toolbar = Toolbar()
        self.layout.addWidget(self.toolbar)

        self.graph = {
            HomeFragment: HomeFragment('홈'),
            AdminFragment: AdminFragment('관리자'),
            DataFragment: DataFragment('데이터 관리'),
            StudentFragment: StudentFragment('학생'),
            ProblemFragment: ProblemFragment('문제'),
            AddProblemFragment: AddProblemFragment('문제 추가') 
        } 
        self.navigation = Navigation(self.layout, self.graph, HomeFragment)
        self.navigation.setup_with_toolbar(self.toolbar)

        self.navigation.navigate(HomeFragment)

    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        if event.key() == Qt.Key_Escape:
            self.navigation.navigate_back()

    def set_stylesheet(self):
        with open('update_style.qss') as f:
            self.setStyleSheet(f.read())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    font_id = QFontDatabase.addApplicationFont('./fonts/hakyo_R.ttf')
    app.setFont(QFont(QFontDatabase.applicationFontFamilies(font_id)[0]))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

