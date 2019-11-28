
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QVBoxLayout, QGroupBox, QLabel, QPushButton, QFormLayout
from gi.repository import Gio
from aqt import preferencedialog



class Preferences(QtWidgets.QWidget):
    def __init__(self, appctxt):
        super().__init__()
        self.appctxt = appctxt
        uic.loadUi(appctxt.get_resource("preferences.ui"), self)
        for app in self.get_apps():
            button = QPushButton(app)
            self.app = app
            button.clicked.connect(self.preference_decorator(app))
            self.formLayout.addRow(button)
        # self.formLayout.setContentsMargins(0,0,0,0)

        self.show()

    def get_apps(self):
        return [app.get_display_name() for app in Gio.app_info_get_all()
                if app.should_show()]

    def preference_decorator(self, app_name):
        ctxt = self.appctxt
        def get_preference_dialog(self):
            appctxt = ctxt
            app = app_name
            # TODO maybe get rid of this decorator approach
            dialog = preferencedialog.PreferenceDialog(appctxt, app)
            if dialog.exec_() == 1:
                print(dialog.time_edit())
                # TODO connect response from update to save and update config
        return get_preference_dialog
