from PyQt6.QtWidgets import QMessageBox


class PromptDialog(QMessageBox):
    def __init__(self, title, msg):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(msg)
        self.exec()
