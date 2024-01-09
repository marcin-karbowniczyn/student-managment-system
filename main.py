import sys
import sqlite3

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar
from PyQt6.QtGui import QAction, QIcon


# Create a cursor to a SQL database. Using connection.execute instead of cursor.execute() would be a 'non-standard shortcut'.
# cursor = sqlite3.connect('database.db').cursor()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Managment System')
        # self.setMinimumSize(800, 600)
        self.resize(QSize(800, 600))
        # self.resize(300, 300)

        # 1. Create a Menu Bar
        # &NAME -> convention
        file_menu = self.menuBar().addMenu('&File')
        help_menu = self.menuBar().addMenu('&Help')
        edit_menu = self.menuBar().addMenu('&Edit')

        # self will connect QAction to the actual class (Main Window)
        add_student_action = QAction(QIcon('icons/add.png'), 'Add Student', self)
        add_student_action.triggered.connect(self.insert)
        file_menu.addAction(add_student_action)

        search_action = QAction(QIcon('icons/search.png'), 'Search Student', self)
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

        # 3. Create a toolbar and add toolbar elements with icons
        toolbar = QToolBar()
        # toolbar.setMovable(True)
        self.addToolBar(toolbar)  # self == main_window object
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

    def load_data(self):
        connection = sqlite3.connect('database.db')
        result = connection.execute('SELECT * FROM students')  # Connection will create cursor every time. Since we have only one operation, it's ok to use connection instead of cursor.
        self.table.setRowCount(0)
        for row_id, row in enumerate(result):
            self.table.insertRow(row_id)
            for column_id, data in enumerate(row):
                self.table.setItem(row_id, column_id, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog(self.load_data)
        dialog.exec()  # This shows the window on the screen. Similar to show() but used for Dialog Windows.

    def search(self):
        dialog = SearchDialog()
        dialog.exec()


# This class in PyQt creates dialog windows
class InsertDialog(QDialog):
    def __init__(self, load_data_callback):
        super().__init__()
        self.load_data = load_data_callback

        self.setWindowTitle('Insert Student Data')
        self.setFixedWidth(410)
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
        try:
            name = self.student_name.text().title()
            course = self.course_name.currentText()
            mobile = self.mobile.text()
            connection = sqlite3.connect('database.db')
            connection.execute('INSERT INTO students (name, course, mobile) VALUES (?,?,?)', (name, course, mobile))
            connection.commit()
            connection.close()
            self.load_data()
            self.close()
        except Exception as e:
            print(e)


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search Student')
        self.setFixedWidth(600)
        self.setFixedHeight(300)

        # 1. Define a layout
        self.layout = QVBoxLayout()

        # 2. Add name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Name')
        self.layout.addWidget(self.name_input)

        # 3. Add search btn
        self.search_btn = QPushButton('Search')
        self.search_btn.clicked.connect(self.search)
        self.layout.addWidget(self.search_btn)

        # 4. Add search result
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(('ID', 'Name', 'Course', 'Mobile'))
        self.result_table.verticalHeader().setVisible(False)
        self.result_table.hide()
        self.layout.addWidget(self.result_table)

        self.setLayout(self.layout)

    def search(self):
        # Two ways of searching for data, either in SQL database or by using QTableWidget search functionalities.
        try:
            name = self.name_input.text().title()
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM students WHERE name=?", (name,))
            result = cursor.fetchone()
        except Exception as e:
            print(e)
            exit()

        if not result:
            prompt = PromptDialog('No students have been found.')
            prompt.exec()
        else:
            self.result_table.setRowCount(0)
            self.result_table.insertRow(0)
            self.result_table.show()
            for column, item in enumerate(result):
                item = QTableWidgetItem(str(item))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.result_table.setItem(0, column, item)
        cursor.close()
        connection.close()

        # name = self.student_name.text()
        # items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        # for item in items:
        #     print(item)
        #     main_window.table.item(item.row(), 1).setSelected(True)


class PromptDialog(QDialog):
    def __init__(self, msg):
        super().__init__()
        self.setWindowTitle('Prompt')
        self.setFixedWidth(200)
        self.setFixedHeight(50)

        layout = QVBoxLayout()

        message_label = QLabel()
        message_label.setText(msg)
        layout.addWidget(message_label)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    main_window.load_data()

    sys.exit(app.exec())
