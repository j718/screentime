# work-around for https://github.com/pyinstaller/pyinstaller/issues/4064
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from screentime import app
import logging


def setup_custom_logger(name):
    formatter = logging.Formatter(
                    fmt='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(screen_handler)
    return logger


def main():
    logger = setup_custom_logger("Screentime")
    appctxt = ApplicationContext()
    ui = appctxt.get_resource("dialog.ui")
    appctxt.app.setQuitOnLastWindowClosed(False)
    appctxt.app.setApplicationName("Screentime")
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
    worker = app.Worker(ui, logger)
    threadpool = QThreadPool()
    threadpool.start(worker)
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
