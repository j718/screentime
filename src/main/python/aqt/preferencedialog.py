
from PyQt5 import QtWidgets, uic


class PreferenceDialog(QtWidgets.QDialog):
    def __init__(self, appctxt, app_name):
        super().__init__()
        self.appctxt = appctxt
        self.app_name = app_name
        # self.windowTitle = self.app_name
        uic.loadUi(self.appctxt.get_resource("preferencedialog.ui"), self)
        # TODO make it so that title of dialog is the app name
        # TODO make it so that time on apps resets at beginning of day

        self.save_button.clicked.connect(self.save)
        self.cancel_button.clicked.connect(self.accept)
        self.app_name_label.setText(self.app_name)


    def save(self):
        """
        invoked by clicking the accept button of the dialog.i
            meant to close app in question
        """
        self.done(1)

    def accept(self):
        """
        invoked by clicking the add time button on the dialog.
            meant to add fifteen minutes until attempting to kill again
        """
        self.done(2)
