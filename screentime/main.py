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

    def set_name(self, name):
        self.app_name.setText(self.get_warning(name))

    def get_warning(self, app_name):
        warning = f"Warning, You have reached your limit for {app_name} today."
        return(warning)

    def accept(self):
        """
        invoked by clicking the accept button of the dialog. meant to close app in question
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

    @pyqtSlot()
    def run(self):
        timer = Screentime()
        window = MyWindow("placeholder")
        while True:
            blocked = timer.apply_limits()
            for x in blocked:
                self.block_app(x.lower(), timer, window)
            time.sleep(5)

    def block_app(self, app_name: str, timer, window):
        """ closes blocked apps """
        if app_name.lower() in str(subprocess.check_output(['wmctrl', '-l'])).lower():

            window.set_name(app_name)
            response = window.exec_()
            if response == 1:
                print(f"Killed {app_name}")
                subprocess.call(['notify-send', f'Closing {app_name}. Limit already reached'])
                subprocess.Popen(["wmctrl", "-c", app_name], bufsize=0)
            elif response == 2:
                timer.increase_limit(app_name)


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    """
    adds a tray icon that can be used to quit
    """
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QtWidgets.QMenu()
        self.exit_action = QAction('Exit Application', self)
        self.exit_action.setStatusTip('Exit the application.')
        self.exit_action.triggered.connect(lambda: QApplication.quit())
        self.menu.addAction(self.exit_action)
        self.setContextMenu(self.menu)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icons/icon.png'))
    QtWidgets.QApplication.setQuitOnLastWindowClosed(False)
    trayIcon = SystemTrayIcon(QtGui.QIcon("icons/icon.png"), app)
    trayIcon.show()

    # start a worker that continually checks if it is time to close
    worker = Worker()
    threadpool = QThreadPool()
    threadpool.start(worker)
    sys.exit(app.exec_())
