from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QComboBox, QPushButton
from classes.DatabaseConnection import DatabaseConnection


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
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute('UPDATE students SET name=?, course=?, mobile=? WHERE id=?',
                       (self.student_name.text(), self.course_name.currentText(), self.mobile.text(), self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        self.main_window_load_data()
        self.close()
