from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QComboBox, QPushButton
from classes.DatabaseConnection import DatabaseConnection


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
            connection = DatabaseConnection().connect()
            connection.execute('INSERT INTO students (name, course, mobile) VALUES (?,?,?)', (name, course, mobile))
            connection.commit()
            connection.close()
            self.main_window_load_data()
            self.close()
        except Exception as e:
            print(e)
