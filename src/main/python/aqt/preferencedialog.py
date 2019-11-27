
from PyQt5 import QtWidgets, uic


class PreferenceDialog(QtWidgets.QDialog):
    def __init__(self, appctxt, app_name):
        super().__init__()
        self.appctxt = appctxt
        self.app_name = app_name
        self.windowTitle = self.app_name
        uic.loadUi(self.appctxt.get_resource("preferencedialog.ui"), self)
        # TODO make it so that title of dialog is the app name
        # TODO make it so that time on apps resets at beginning of day
