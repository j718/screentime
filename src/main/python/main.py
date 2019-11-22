from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
import subprocess
import sys
from screentime import timer, app
# import screentime

def main():
    appctxt = ApplicationContext()
    ui = appctxt.get_resource("dialog.ui")
    # app = QtWidgets.QApplication(sys.argv)
    # appctxt.app.setWindowIcon(QtGui.QIcon('icons/icon.png'))
    QtWidgets.QApplication.setQuitOnLastWindowClosed(False)
    trayIcon = app.SystemTrayIcon(QtGui.QIcon("icons/icon.png"), appctxt.app)
    trayIcon.show()

    # start a worker that continually checks if it is time to close
    worker = app.Worker(ui)
    threadpool = QThreadPool()
    threadpool.start(worker)
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
    # sys.exit(app.exec_())

if __name__ == '__main__':
    # appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    # window = QMainWindow()
    # window.resize(250, 150)
    # window.show()
    # exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    # sys.exit(exit_code)
    main()
