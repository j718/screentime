# TODO make dashboard file
# TODO make dashboard open on startup
# TODO convert list view to tree view for apps
# TODO change edit dialog to preferences window
# TODO setup groups format in timer file

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QVBoxLayout, QGroupBox, QLabel, QPushButton, QFormLayout
from aqt import preferences


class Dashboard(QtWidgets.QWidget):
    def __init__(self, appctxt):
        super().__init__()
        self.appctxt = appctxt
        uic.loadUi(self.appctxt.get_resource("dashboard.ui"), self)
        self.draw()
        # self.windowTitle = self.app_name
        # TODO make it so that title of dialog is the app name
        # TODO make it so that time on apps resets at beginning of day

        # self.save_button.clicked.connect(self.save)
        # self.cancel_button.clicked.connect(self.accept)
        # self.app_name_label.setText(self.app_name)


    def draw(self):
        for i in reversed(range(self.formLayout.count())):
            self.formLayout.itemAt(i).widget().setParent(None)
        sql = 'select title from limit_group'
        groups = self.appctxt.db.connection.execute(sql)
        for group, in groups:
            button = QPushButton(group)
            button.clicked.connect(lambda checked, group=group: self.get_preference_dialog(group))
            self.formLayout.addRow(button)
        self.add_button.clicked.connect(self.get_preference_dialog)

    def get_preference_dialog(self, group=None):
        # TODO maybe get rid of this decorator approach
        dialog = preferences.Preferences(self.appctxt, group)
        if dialog.exec_() == 1:
            self.draw()
            # self.update_config(dialog.app_name, dialog.time_edit.text())

            # TODO connect response from update to save and update config

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
