import yaml
import pandas as pd
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
            button.clicked.connect(lambda checked, app=app: self.get_preference_dialog(app))
            self.formLayout.addRow(button)
        # self.formLayout.setContentsMargins(0,0,0,0)

        self.show()

    def get_apps(self):
        return [app.get_display_name() for app in Gio.app_info_get_all()
                if app.should_show()]

    def get_preference_dialog(self, app_name):
        # TODO maybe get rid of this decorator approach
        dialog = preferencedialog.PreferenceDialog(self.appctxt, app_name)
        if dialog.exec_() == 1:
            self.update_config(dialog.app_name, dialog.time_edit.text())
            # TODO connect response from update to save and update config

    def update_config(self, app_name, limit):
        with self.appctxt.config_path.open('r') as f:
            config_file = yaml.safe_load(f)
        found = False
        for app in config_file:
            if app['id'] == app_name:
                found = True
                app['limit'] = int(limit)

        if not found:
            config_file.append({
                'id':app_name,
                'limit':int(limit)
            })
        with self.appctxt.config_path.open('w') as f:
            yaml.dump(config_file, f)
        # TODO reload config after update
        # TODO update show current limits in preference dialog
        # TODO show current limits in preferences
        # TODO make preference searchable
