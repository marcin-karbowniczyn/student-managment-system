import sys
import sqlite3
import traceback

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar, \
    QGridLayout, QMessageBox
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
        about_action.triggered.connect(self.about)

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

        # 4. Create status bar and add status bar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # 4.1 Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def load_data(self):
        connection = sqlite3.connect('database.db')
        result = connection.execute('SELECT * FROM students')  # Connection will create cursor every time. Since we have only one operation, it's ok to use connection instead of cursor.
        self.table.setRowCount(0)
        for row_id, row in enumerate(result):
            self.table.insertRow(row_id)
            for column_id, data in enumerate(row):
                self.table.setItem(row_id, column_id, QTableWidgetItem(str(data)))
        self.table.resizeColumnToContents(1)
        connection.close()

    def cell_clicked(self):
        edit_btn = QPushButton('Edit')
        edit_btn.clicked.connect(self.edit)

        delete_btn = QPushButton('Delete')
        delete_btn.clicked.connect(self.delete)

        buttons = self.findChildren(QPushButton)
        if buttons:
            for btn in buttons:
                self.statusbar.removeWidget(btn)
                btn.deleteLater()

        self.statusbar.addWidget(edit_btn)
        self.statusbar.addWidget(delete_btn)

    def about(self):
        dialog = AboutDialog()
        dialog.exec()

    def insert(self):
        dialog = InsertDialog(self.load_data)
        dialog.exec()  # This shows the window on the screen. Similar to show() but used for Dialog Windows.

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog(self.table, self.load_data)
        dialog.exec()

    def delete(self):
        try:
            dialog = DeleteDialog(self.table, self.load_data)
            dialog.exec()
        except AttributeError:
            traceback.print_exc()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('About')
        content = """
        This app was created during the course "The Python Mega Course".
        Feel free to modify and reuse this app.
        """
        self.setText(content)


# This class in PyQt creates dialog windows
class InsertDialog(QDialog):
    def __init__(self, load_data_callback):
        super().__init__()
        self.main_window_load_data = load_data_callback

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
            self.main_window_load_data()
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
            cursor.execute(f"SELECT * FROM students WHERE name LIKE '{name}%'")
            result = cursor.fetchall()
        except Exception:
            traceback.print_exc()
            exit()

        if not result:
            PromptDialog('Failed', 'No students have been found.')
        else:
            self.result_table.setRowCount(0)
            for row_id, row in enumerate(result):
                self.result_table.insertRow(row_id)
                for column, item in enumerate(row):
                    item = QTableWidgetItem(str(item))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.result_table.setItem(row_id, column, item)
            self.result_table.show()
            self.result_table.resizeColumnToContents(1)
        cursor.close()
        connection.close()

        # name = self.student_name.text()
        # items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        # for item in items:
        #     print(item)
        #     main_window.table.item(item.row(), 1).setSelected(True)


class EditDialog(QDialog):
    def __init__(self, main_window_table, load_data_callback):
        super().__init__()
        self.main_window_table = main_window_table
        self.main_window_load_data = load_data_callback

        self.setWindowTitle('Update Student Data')
        self.setFixedWidth(410)
        self.setFixedHeight(300)

        # 1. Define layout to be QVBoxLayout() (we only need one vertical column of widgets)
        layout = QVBoxLayout()

        # 2. Get student name from selected row
        row_index = main_window_table.currentRow()  # Returns an index of the row that is currently highlighted

        # 2.1 Get student id
        self.student_id = main_window_table.item(row_index, 0).text()

        student_name = main_window_table.item(row_index, 1).text()
        # 2.2 Add student name input
        self.student_name = QLineEdit(student_name)
        layout.addWidget(self.student_name)

        # 3. Get course name from selected row
        course_name = main_window_table.item(row_index, 2).text()
        # 3.1 Add combo box with courses
        self.course_name = QComboBox()
        courses = ['Biology', 'Math', 'Astronomy', 'Physics']
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # 4. Get mobile number from selected row
        student_mobile = main_window_table.item(row_index, 3).text()
        # 4.1 Add mobile number input
        self.mobile = QLineEdit(student_mobile)
        layout.addWidget(self.mobile)

        # 5. Add submit button
        submit_btn = QPushButton('Update')
        submit_btn.clicked.connect(self.update_student)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE students SET name=?, course=?, mobile=? WHERE id=?',
                       (self.student_name.text(), self.course_name.currentText(), self.mobile.text(), self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        self.main_window_load_data()
        self.close()


class DeleteDialog(QDialog):
    def __init__(self, main_window_table, load_data_callback):
        super().__init__()
        self.main_window_table = main_window_table
        self.main_window_load_data = load_data_callback

        self.setWindowTitle('Delete Student Data')

        row_index = main_window_table.currentRow()  # Returns an index of the row that is currently highlighted/clicked
        self.student_id = main_window_table.item(row_index, 0).text()
        student_name = main_window_table.item(row_index, 1).text()

        layout = QGridLayout()
        confirmation = QLabel(f'Are you sure you want to delete the Student: {student_name}?')
        yes_btn = QPushButton('Yes')
        yes_btn.clicked.connect(self.delete_student)
        no_btn = QPushButton('No')
        no_btn.clicked.connect(self.close)

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes_btn, 1, 0)
        layout.addWidget(no_btn, 1, 1)
        self.setLayout(layout)

    def delete_student(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute(f'DELETE from students WHERE id=?', (self.student_id,))
        connection.commit()

        cursor.close()
        connection.close()

        self.main_window_load_data()
        self.close()

        PromptDialog('Success', 'The record was deleted successfully!')


class PromptDialog(QMessageBox):
    def __init__(self, title, msg):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(msg)
        self.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    main_window.load_data()

    sys.exit(app.exec())
