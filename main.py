import sys
import sqlite3

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox
from PyQt6.QtGui import QAction


# Create a cursor to a SQL database. Using connection.execute instead of cursor.execute() would be a 'non-standard shortcut'.
# cursor = sqlite3.connect('database.db').cursor()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Managment System')

        # 1. Create a Menu Bar
        # & -> convention
        file_menu = self.menuBar().addMenu('&File')
        help_menu = self.menuBar().addMenu('&Help')
        edit_menu = self.menuBar().addMenu('&Edit')

        # self will connect QAction to the actual class (Main Window)
        add_student_action = QAction('Add Student', self)
        add_student_action.triggered.connect(self.insert)
        file_menu.addAction(add_student_action)

        search_action = QAction('Search Student', self)
        search_action.triggered.connect(self.search)
        edit_menu.addAction(search_action)

        about_action = QAction('About', parent=self)
        help_menu.addAction(about_action)

        # 2. Create a table with students
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('ID', 'Name', 'Course', 'Mobile'))
        self.table.verticalHeader().setVisible(False)  # It hides the built-in id columns
        # We use this instead of layout(grid) from the previous app. Sets the given widget to be the main window’s central widget.
        # There is no layout on QMainWindow Class, it has a menu, toolbar and a central widget.
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect('database.db')
        result = connection.execute('SELECT * FROM students')  # Connection will create cursor every time. Since we have only one operation, it's ok to use connection instead of cursor.
        self.table.setRowCount(0)
        for row_id, row in enumerate(result):
            self.table.insertRow(row_id)
            for column_id, data in enumerate(row):
                self.table.setItem(row_id, column_id, QTableWidgetItem(str(data)))
        connection.close()

    @classmethod
    def insert(cls):
        dialog = InsertDialog()
        dialog.exec()  # This shows the window on the screen. Similar to show() but used for Dialog Windows.

    @classmethod
    def search(cls):
        dialog = SearchDialog()
        dialog.exec()


# This class in PyQt creates dialog windows
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Insert Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # 1. Define layout to be QVBoxLayout() (we only need one vertical column of widgets)
        layout = QVBoxLayout()

        # 2. Add student name input
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        # 3. Add combo box with courses
        self.course_name = QComboBox()
        courses = ['Biology', 'Math', 'Astronomy', 'Physics']
        self.course_name.addItems(courses)
        self.course_name.setPlaceholderText('Courses')
        layout.addWidget(self.course_name)

        # 4. Add mobile number input
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText('Phone number')
        layout.addWidget(self.mobile)

        # 5. Add submit button
        submit_btn = QPushButton('Submit')
        submit_btn.clicked.connect(self.add_student)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.currentText()
        mobile = self.mobile.text()
        connection = sqlite3.connect('database.db')
        connection.execute('INSERT INTO students (name, course, mobile) VALUES (?,?,?)', (name, course, mobile))
        connection.commit()
        connection.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search Student')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # 1. Define a laout
        layout = QVBoxLayout()

        # 2. Add name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Name')
        layout.addWidget(self.name_input)

        # 3. Add search btn
        self.search_btn = QPushButton('Search')
        self.search_btn.clicked.connect(self.search)
        layout.addWidget(self.search_btn)

        # 4. Add search result
        self.search_result = QLabel('')
        layout.addWidget(self.search_result)

        self.setLayout(layout)

    def search(self):
        # Two ways of searching for data, either in SQL database or by using QTableWidget search functionalities.
        name = self.name_input.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM students WHERE name=?', (name,))
        index, name, course, mobile = cursor.fetchone()
        self.search_result.setText(f"""
        Index: {index},
        Name: {name},
        Course: {course},
        Mobile Number: {mobile}
        """)
        cursor.close()
        connection.close()

        # name = self.student_name.text()
        # items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        # for item in items:
        #     print(item)
        #     main_window.table.item(item.row(), 1).setSelected(True)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
