from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot, QRunnable
from .timer import Screentime
import time
import subprocess


class MyWindow(QtWidgets.QDialog):
    def __init__(self, app_name: str, qt_creator_file):
        # QtWidgets.QMainWindow.__init__(self)
        super().__init__()
        uic.loadUi(qt_creator_file, self)
        # self.show()
        # self.setupUi(self)
        self.app_name.setText(self.get_warning(app_name))

        self.accept_button.clicked.connect(self.accept)
        self.add_button.clicked.connect(self.add)

    def set_name(self, name):
        self.app_name.setText(self.get_warning(name))

    def get_warning(self, app_name):
        warning = f"Warning, You have reached your limit for {app_name} today."
        return(warning)

    def accept(self):
        """
        invoked by clicking the accept button of the dialog.i
         meant to close app in question
        """
        self.done(1)

    def add(self):
        """
        invoked by clicking the add time button on the dialog.
         meant to add fifteen minutes until attempting to kill again
        """
        self.done(2)


class Worker(QRunnable):
    """
    Worker thread
    """
    def __init__(self, ui_path, logger, *args, **kwargs):
        super(Worker, self).__init__()
        self.logger = logger
        self.window = MyWindow("placeholder", ui_path)

    @pyqtSlot()
    def run(self):
        timer = Screentime(self.logger)
        while True:
            blocked = timer.apply_limits()
            for x in blocked:
                self.block_app(x.lower(), timer, self.window)
            time.sleep(5)

    def block_app(self, app_name: str, timer, window):
        """ closes blocked apps """
        app_list = str(subprocess.check_output(['wmctrl', '-l'])).lower()
        if app_name.lower() in app_list:
            self.window.set_name(app_name)
            response = self.window.exec_()
            if response == 1:
                self.logger.info(f"Killed {app_name}")
                subprocess.call(['notify-send',
                                 f'Closing {app_name}. Limit already reached'])
                subprocess.Popen(["wmctrl", "-c", app_name], bufsize=0)
            elif response == 2:
                timer.increase_limit(app_name)
