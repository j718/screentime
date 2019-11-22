import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from app import Screentime
import time
import subprocess

qtcreator_file = "screentime/dialog.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


class MyWindow(QtWidgets.QDialog, Ui_MainWindow):
    def __init__(self, app_name: str):
        # QtWidgets.QMainWindow.__init__(self)
        QtWidgets.QDialog.__init__(self)

        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.app_name.setText(self.get_warning(app_name))

        self.accept_button.clicked.connect(self.accept)
        self.add_button.clicked.connect(self.add)

    def get_warning(self, app_name):
        warning = f"Warning, You have reached your limit for {app_name} today."
        return(warning)

    def accept(self):
        self.done(0)

    def add(self):
        self.done(1)

class Worker(QRunnable):
    """
    Worker thread"""

    # def __init__(self, window, *args, **kwargs):
    #     super(Worker, self).__init__()

    @pyqtSlot()
    def run(self):
        app = Screentime()
        while True:
            blocked = app.apply_limits()
            for x in blocked:
                self.block_app(x.lower())
            time.sleep(5)

    def block_app(self, app_name: str):
        """ closes blocked apps """
        if app_name.lower() in str(subprocess.check_output(['wmctrl', '-l'])).lower():
            window = MyWindow(app_name)
            window.exec_()
            print(f"Killed {app_name}")
            subprocess.call(['notify-send', f'Closing {app_name}. Limit already reached'])
            # subprocess.Popen(["wmctrl", "-c", app_name], bufsize=0)

# def block_app(window, app_name: str):
#     """ closes blocked apps """
#     if app_name.lower() in str(subprocess.check_output(['wmctrl', '-l'])).lower():
#         window.exec_()
#         subprocess.call(['notify-send', f'Closing {app_name}. Limit already reached'])
#         subprocess.Popen(["wmctrl", "-c", app_name], bufsize=0)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setQuitOnLastWindowClosed(False)
    trayIcon = QtWidgets.QSystemTrayIcon(QtGui.QIcon("icons/icon.png"), app)
    trayIcon.show()
    worker = Worker()
    threadpool = QThreadPool()
    threadpool.start(worker)
    # window.show()
    # block_app(window, "anki")
    # block_app(window, "hyper")
    sys.exit(app.exec_())
