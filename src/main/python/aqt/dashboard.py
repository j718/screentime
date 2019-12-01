from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QVBoxLayout, QGroupBox, QLabel, QPushButton, QFormLayout
from aqt import preferences


class Dashboard(QtWidgets.QWidget):
    def __init__(self, appctxt):
        super().__init__()
        self.appctxt = appctxt
        uic.loadUi(self.appctxt.get_resource("dashboard.ui"), self)
        self.add_button.clicked.connect(self.get_preference_dialog)
        self.draw()
        # TODO make it so that title of dialog is the app name
        # TODO make it so that time on apps resets at beginning of day

    def draw(self):
        for i in reversed(range(self.formLayout.count())):
            self.formLayout.itemAt(i).widget().setParent(None)
        sql = 'select title from limit_group'
        groups = self.appctxt.db.connection.execute(sql)
        for group, in groups:
            button = QPushButton(group)
            button.clicked.connect(lambda checked, group=group: self.get_preference_dialog(group))
            self.formLayout.addRow(button)

    def get_preference_dialog(self, group=None):
        dialog = preferences.Preferences(self.appctxt, group)
        if dialog.exec_() == 1:
            self.draw()
