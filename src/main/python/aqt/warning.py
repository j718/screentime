from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


class Warning(QDialog):
    def __init__(self, appctxt):
        super().__init__()
        self.appctxt = appctxt
        self.app = appctxt.app
        self.form = self.appctxt.get_resource('warning.ui')
        uic.loadUi(self.form, self)
        # TODO finish designing UI

