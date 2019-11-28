# TODO make dashboard file
# TODO make dashboard open on startup
# TODO convert list view to tree view for apps
# TODO change edit dialog to preferences window
# TODO setup groups format in timer file

from PyQt5 import QtWidgets, uic


class Dashboard(QtWidgets.QWidget):
    def __init__(self, appctxt):
        super().__init__()
        self.appctxt = appctxt
        # self.windowTitle = self.app_name
        uic.loadUi(self.appctxt.get_resource("dashboard.ui"), self)
        # TODO make it so that title of dialog is the app name
        # TODO make it so that time on apps resets at beginning of day

        # self.save_button.clicked.connect(self.save)
        # self.cancel_button.clicked.connect(self.accept)
        # self.app_name_label.setText(self.app_name)


    # def save(self):
    #     """
    #     invoked by clicking the accept button of the dialog.i
    #         meant to close app in question
    #     """
    #     self.done(1)

    # def accept(self):
    #     """
    #     invoked by clicking the add time button on the dialog.
    #         meant to add fifteen minutes until attempting to kill again
    #     """
    #     self.done(2)
