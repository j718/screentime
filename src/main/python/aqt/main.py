from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
import aqt.webview
from PyQt5 import QtWidgets, uic
import aqt.toolbar

class ScreentimeQt(QMainWindow):
    def __init__(self, appctxt):
        super().__init__()

        self.appctxt = appctxt
        self.app = appctxt.app
        self.web = aqt.webview.STWebView()
        self.app.mw = self
        self.setupMainWindow()

    # def setupUI():



    # Main window setup
    ##########################################################################

    def setupMainWindow(self):
        # main window
        self.form = self.appctxt.get_resource("mainwindow.ui")
        # self.form.setupUi(self)
        uic.loadUi(self.form, self)
        # toolbar
        tweb = self.toolbarWeb = aqt.webview.STWebView()
        tweb.title = "top toolbar"
        self.toolbar = aqt.toolbar.Toolbar(self, tweb)
        self.toolbar.draw()
        # # main area
        # add in a layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.addWidget(tweb)
        # self.mainLayout.addWidget(self.web)
        # self.mainLayout.addWidget(sweb)
        self.centralwidget.setLayout(self.mainLayout)

    def setupMenus(self):
        self.action_about.triggered(self.onAbout)
        # TODO finish connecting about
        # TODO finish designing about

    def onAbout(self):

