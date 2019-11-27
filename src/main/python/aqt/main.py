from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QSystemTrayIcon, QMenu, QAction
import sys
from PyQt5 import uic
from aqt import about, worker
from PyQt5.QtCore import QThreadPool


class ScreentimeQt(QMainWindow):
    def __init__(self, appctxt):
        super().__init__()

        self.appctxt = appctxt
        self.app = appctxt.app
        self.app.mw = self
        self.worker = worker.Worker(appctxt)
        self.threadpool = QThreadPool()
        self.threadpool.start(self.worker)

        self.appctxt.app.setQuitOnLastWindowClosed(False)
        self.appctxt.app.setApplicationName("Screentime")

        self.setup_mw()
        self.setup_tray()

    def setup_mw(self):
        """
        creates the main window of the application
        """
        # main window
        self.form = self.appctxt.get_resource("mainwindow.ui")
        uic.loadUi(self.form, self)

        # add in a layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.centralwidget.setLayout(self.mainLayout)
        self.setup_menus()

    def setup_menus(self):
        self.action_about.triggered.connect(self.onAbout)
        # TODO finish designing about

    def onAbout(self):
        dialog = about.About(self.appctxt)
        dialog.exec_()

    def setup_tray(self):
        """
        create the system tray icon
        """
        tray = QSystemTrayIcon(self.appctxt.app_icon, self.appctxt.app)
        tray.setVisible(True)

        # create tray menu
        t_menu = QMenu()
        exit_action = QAction('Exit Application', tray)
        exit_action.setStatusTip('Exit the application.')
        exit_action.triggered.connect(lambda: sys.exit(0))
        t_menu.addAction(exit_action)
        tray.setContextMenu(t_menu)

# TODO test that activity watch is running on startup
