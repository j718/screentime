
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot, QRunnable
import time
import subprocess


class Config_Window(QtWidgets.QDialog):
    def __init__(self, appctxt):
        super().__init__()
        uic.loadUi(appctxt.get_resource("config.ui"), self)
        config = ["lthis", "that"]
        # self.listView.addItem("bla")

        # self.config_list.add_item(config)
