import sys
import traceback

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QToolBar, QStatusBar
from PyQt6.QtGui import QAction, QIcon

from classes.DatabaseConnection import DatabaseConnection
from classes.AboutDialog import AboutDialog
from classes.InsertDialog import InsertDialog
from classes.SearchDialog import SearchDialog
from classes.EditDialog import EditDialog
from classes.DeleteDialog import DeleteDialog


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
        connection = DatabaseConnection().connect()
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    main_window.load_data()

    sys.exit(app.exec())
