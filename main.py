import sys

from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget
from PyQt6.QtGui import QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Managment System')

        # 1. Create a Menu Bar
        # & -> convention
        file_menu = self.menuBar().addMenu('&File')
        help_menu = self.menuBar().addMenu('&Help')

        # self will connect QAction to the actual class (Main Window)
        add_student_action = QAction('Add Student', parent=self)
        file_menu.addAction(add_student_action)

        about_action = QAction('About', parent=self)
        help_menu.addAction(about_action)

        # 2. Create a table with students
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('ID', 'Name', 'Course', 'Mobile'))
        self.setCentralWidget(self.table)  # We use this instead of layout(grid) from the previous app. Sets the given widget to be the main window’s central widget.

    def load_data(self):
        self.table


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
