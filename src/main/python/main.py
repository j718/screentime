# work-around for https://github.com/pyinstaller/pyinstaller/issues/4064
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from screentime import app


def main():
    appctxt = ApplicationContext()
    ui = appctxt.get_resource("dialog.ui")
    appctxt.app.setQuitOnLastWindowClosed(False)
    tray = QSystemTrayIcon(appctxt.app_icon, appctxt.app)
    tray.setVisible(True)

    # create tray menu
    menu = QMenu()
    exit_action = QAction('Exit Application', tray)
    exit_action.setStatusTip('Exit the application.')
    exit_action.triggered.connect(lambda: sys.exit(0))
    menu.addAction(exit_action)
    tray.setContextMenu(menu)

    # start a worker that continually checks if it is time to close
    worker = app.Worker(ui)
    threadpool = QThreadPool()
    threadpool.start(worker)
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
