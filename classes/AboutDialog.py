from PyQt6.QtWidgets import QMessageBox


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('About')
        content = """
        This app was created during the course "The Python Mega Course".
        Feel free to modify and reuse this app.
        """
        self.setText(content)
