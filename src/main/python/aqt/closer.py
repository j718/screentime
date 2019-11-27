from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt


class Closer(QtWidgets.QDialog):
    def __init__(self, appctxt):
        super().__init__()
        self.appctxt = appctxt
        self.app = appctxt.app
        self.form = self.appctxt.get_resource('closer.ui')
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        uic.loadUi(self.form, self)

        # connect buttons
        self.accept_button.clicked.connect(self.accept)
        self.add_button.clicked.connect(self.add)

    def set_warning(self, app_name: str, time: str):
        warning = f"Warning: You have reached your limit of {time}"\
                    f" minutes for {app_name} today."
        self.app_name.setText(warning)

    def accept(self):
        """
        invoked by clicking the accept button of the dialog.i
            meant to close app in question
        """
        self.done(1)

    def add(self):
        """
        invoked by clicking the add time button on the dialog.
            meant to add fifteen minutes until attempting to kill again
        """
        self.done(2)
