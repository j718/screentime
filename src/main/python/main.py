# work-around for https://github.com/pyinstaller/pyinstaller/issues/4064
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys
from PyQt5.QtCore import QThreadPool
from screentime import app


def main():
    appctxt = ApplicationContext()
    ui = appctxt.get_resource("dialog.ui")
    appctxt.app.setQuitOnLastWindowClosed(False)
    trayIcon = app.SystemTrayIcon(appctxt.app_icon, appctxt.app)
    trayIcon.setVisible(True)

    # start a worker that continually checks if it is time to close
    worker = app.Worker(ui)
    threadpool = QThreadPool()
    threadpool.start(worker)
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
