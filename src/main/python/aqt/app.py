
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt


class App(QtWidgets.QDialog):
    def __init__(self, appctxt):
        super().__init__()
        self.appctxt = appctxt
        self.app = appctxt.app
        self.form = self.appctxt.get_resource('app.ui')
        uic.loadUi(self.form, self)

        # connect buttons
        self.accept_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.cancel)
        # self.add_button.clicked.connect(self.add)

    def accept(self):
        """
        invoked by clicking the accept button of the dialog.i
            meant to close app in question
        """
        self.done(1)

    def cancel(self):
        """
        invoked by clicking the accept button of the dialog.i
            meant to close app in question
        """
        self.done(0)
