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

class MainWindow(QMainWindow):

    back_stack: list[Fragment]
    current_fragment: Fragment = None

    layout: QVBoxLayout
    layout_toolbar: QHBoxLayout
    title_toolbar: QLabel
    button_back: QPushButton

    home_fragment: HomeFragment
    home_view_model: HomeViewModel

    admin_fragment: AdminFragment
    admin_view_model: AdminViewModel

    data_fragment: DataFragment
    data_view_model: DataViewModel

    student_fragment: StudentFragment
    student_view_model: StudentViewModel

    problem_fragment: ProblemFragment
    problem_view_model: ProblemViewModel

    add_problem_fragment: AddProblemFragment
    add_problem_view_model: AddProblemViewModel


    def __init__(self):
        super().__init__()
        self.set_stylesheet()
        
        self.setWindowTitle("BrainScan")
        self.setGeometry(0, 0, 1280, 720)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        self.setup_toolbar()

        self.home_view_model = HomeViewModel()
        self.home_fragment = HomeFragment("홈", self.home_view_model)

        self.admin_view_model = AdminViewModel()
        self.admin_fragment = AdminFragment("관리자", self.admin_view_model)

        self.data_view_model = DataViewModel()
        self.data_fragment = DataFragment("데이터 관리", self.data_view_model)

        self.student_view_model = StudentViewModel()
        self.student_fragment = StudentFragment("학생", self.student_view_model)

        self.problem_view_model = ProblemViewModel()
        self.problem_fragment = ProblemFragment("문제", self.problem_view_model)

        self.add_problem_view_model = AddProblemViewModel()
        self.add_problem_fragment = AddProblemFragment("문제 추가", self.add_problem_view_model)

        self.back_stack = list()
        self.navigate(self.home_fragment)

        # event handling
        self.home_view_model.event.connect(self.on_home_event)
        self.admin_view_model.event.connect(self.on_admin_event)
        self.data_view_model.event.connect(self.on_data_event)
        self.student_view_model.event.connect(self.on_student_event)
        self.problem_view_model.event.connect(self.on_problem_event)

    def setup_toolbar(self):
        self.layout_toolbar = QHBoxLayout()
        self.layout.addLayout(self.layout_toolbar)

        self.button_back = QPushButton('< ')
        self.button_back.setObjectName('back')
        self.button_back.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.button_back.clicked.connect(self.navigate_back)
        self.layout_toolbar.addWidget(self.button_back)

        self.title_toolbar = QLabel()
        self.title_toolbar.setObjectName('title')
        self.layout_toolbar.addWidget(self.title_toolbar)

    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        if event.key() == Qt.Key_Escape:
            self.navigate_back()

    def navigate(self, fragment: QWidget):
        if self.current_fragment is not None:
            self.back_stack.append(self.current_fragment)
            self.layout.removeWidget(self.current_fragment)
            self.current_fragment.setParent(None)

        self.current_fragment = fragment
        self.layout.addWidget(self.current_fragment)
        self.on_screen_change()

    def navigate_back(self):
        if len(self.back_stack) > 0:
            self.layout.removeWidget(self.current_fragment)
            self.current_fragment.setParent(None)
            
            fragment = self.back_stack.pop()
            self.current_fragment = fragment
            self.layout.addWidget(self.current_fragment)
            self.on_screen_change()

    def on_screen_change(self):
        self.current_fragment.on_resume()

        self.title_toolbar.show()
        self.button_back.show()
        self.layout_toolbar.setContentsMargins(20, 16, 20, 16)

        if self.current_fragment == self.home_fragment:
            self.title_toolbar.hide()
            self.button_back.hide()
            self.layout_toolbar.setContentsMargins(0, 0, 0, 0)

        if len(self.back_stack) == 0:
            self.button_back.hide()
        else:
            self.button_back.show()
        
        self.title_toolbar.setText(self.current_fragment.title)

    def on_home_event(self, event):
        if isinstance(event, HomeViewModel.NavigateToAdminScreen):
            self.navigate(self.admin_fragment)

    def on_admin_event(self, event):
        if isinstance(event, AdminViewModel.NavigateBack):
            self.navigate_back()
        elif isinstance(event, AdminViewModel.NavigateToDataFragment):
            self.navigate(self.data_fragment)
        elif isinstance(event, AdminViewModel.NavigateToStudentFragment):
            self.navigate(self.student_fragment)
        elif isinstance(event, AdminViewModel.NavigateToProblemFragment):
            self.navigate(self.problem_fragment)

    def on_data_event(self, event):
        if isinstance(event, DataViewModel.NavigateBack):
            self.navigate_back()

    def on_student_event(self, event):
        pass

    def on_problem_event(self, event):
        if isinstance(event, ProblemViewModel.NavigateToAddProblem):
            self.add_problem_fragment.set_problem_header(event.header)
            self.navigate(self.add_problem_fragment)

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

