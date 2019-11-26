from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


class About(QDialog):
    def __init__(self, appctxt):
        super().__init__()
        self.appctxt = appctxt
        self.app = appctxt.app
        self.form = self.appctxt.get_resource('about.ui')
        uic.loadUi(self.form, self)
        # TODO finish designing UI

