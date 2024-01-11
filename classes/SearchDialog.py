import traceback
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from classes.DatabaseConnection import DatabaseConnection
from classes.PromptDialog import PromptDialog


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
            connection = DatabaseConnection().connect()
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
