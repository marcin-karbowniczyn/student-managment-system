from PyQt6.QtWidgets import QDialog, QPushButton, QGridLayout, QLabel
from classes.DatabaseConnection import DatabaseConnection
from classes.PromptDialog import PromptDialog


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
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute(f'DELETE from students WHERE id=?', (self.student_id,))
        connection.commit()

        cursor.close()
        connection.close()

        self.main_window_load_data()
        self.close()

        PromptDialog('Success', 'The record was deleted successfully!')
