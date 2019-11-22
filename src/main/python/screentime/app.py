from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot, QRunnable
from .timer import Screentime
import time
import subprocess


class MyWindow(QtWidgets.QDialog):
    def __init__(self, qt_creator_file):
        super().__init__()
        uic.loadUi(qt_creator_file, self)

        self.accept_button.clicked.connect(self.accept)
        self.add_button.clicked.connect(self.add)

    def set_warning(self, app_name, time):
        warning = f"Warning: You have reached your limit of {time}"\
                  f" minutes for {app_name} today."
        self.app_name.setText(warning)

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
        self.window = MyWindow(ui_path)

    @pyqtSlot()
    def run(self):
        timer = Screentime(self.logger)
        while True:
            blocked = timer.apply_limits()
            for index, row in blocked.iterrows():
                self.block_app(row.id.lower(), timer, self.window, row.limit)
            time.sleep(5)

    def block_app(self, app_name: str, timer, window, time):
        """ closes blocked apps """
        app_list = str(subprocess.check_output(['wmctrl', '-l'])).lower()
        if app_name.lower() in app_list:
            self.window.set_warning(app_name, time)
            self.logger.info(f"Sending warning for {app_name}")
            response = self.window.exec_()
            if response == 1:
                self.logger.info(f"Killed {app_name}")
                subprocess.call(['notify-send',
                                 f'Closing {app_name}. Time limit reached.'])
                subprocess.Popen(["wmctrl", "-c", app_name], bufsize=0)
            elif response == 2:
                timer.increase_limit(app_name)
