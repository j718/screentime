from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt


class Closer(QtWidgets.QDialog):
    def __init__(self, appctxt):
        super().__init__()
        self.appctxt = appctxt
        self.app = appctxt.app
        self.form = self.appctxt.get_resource('closer.ui')
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowState(Qt.WindowFullScreen)
        uic.loadUi(self.form, self)

        # connect buttons
        self.accept_button.clicked.connect(self.accept)
        # self.add_button.clicked.connect(self.add)

# TODO only allow one instance of hte app
    def set_warning(self, app_name: str, time: str):
        warning = f"Reached limit of {time}"\
                    f" minutes for {app_name} today."
        self.app_name.setText(warning)

    def accept(self):
        """
        invoked by clicking the accept button of the dialog.i
            meant to close app in question
        """
        self.done(1)
