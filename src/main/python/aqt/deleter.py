from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt


class Delete(QtWidgets.QDialog):
    def __init__(self, appctxt):
        super().__init__()
        self.appctxt = appctxt
        self.app = appctxt.app
        self.form = self.appctxt.get_resource('delete.ui')
        uic.loadUi(self.form, self)

        # connect buttons
        self.delete_button.clicked.connect(self.delete)
        self.cancel_button.clicked.connect(self.cancel)
        # self.add_button.clicked.connect(self.add)

    def delete(self):
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

    # def add(self):
    #     """
    #     invoked by clicking the add time button on the dialog.
    #         meant to add fifteen minutes until attempting to kill again
    #     """
    #     self.done(2)
