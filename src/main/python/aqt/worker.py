from PyQt5.QtCore import pyqtSlot, QRunnable
from utils.timer import Screentime
import time
import subprocess
from aqt.closer import Closer
import signal
import os
from gi.repository import Wnck


class Worker(QRunnable):
    """
    Worker thread
    """
    def __init__(self, appctxt, *args, **kwargs):
        super().__init__()
        self.appctxt = appctxt
        self.app = appctxt.app
        self.closer = Closer(self.appctxt)
        self.timer = Screentime(appctxt)
        self.screen = Wnck.Screen.get_default()
        self.screen.force_update()

    @pyqtSlot()
    def run(self):
        while True:
            self.block_apps()
            time.sleep(10)
            # make sure that tray is showing
            # TODO increase increment based on which is closest to rnning out
            # TODO finish making tray work on startup

    def block_apps(self):
        """ closes blocked apps """
        blocked = self.timer.apply_limits()
        app_list = [x.get_application() for x in self.screen.get_windows()]
        for app in app_list:
            if blocked.app.str.lower().isin([app.get_name().lower()]).any():
                # self.closer.set_warning(row.title, row.time_limit)

                row = blocked[blocked.app.str.lower().isin([app.get_name().lower()])]
                limit = (row.time_limit.iloc[0])
                self.closer.set_warning(app.get_name(), limit)
                self.appctxt.logger.info(f"Sending warning for {app.get_name()}")
                response = self.closer.exec_()
                if response == 1:
                    self.appctxt.logger.info(f"Killed {app.get_name()}")
                    subprocess.call(['notify-send',
                                    f'Closing {app.get_name()}. Time limit reached.'])
                    os.kill(app.get_pid(), signal.SIGKILL)
                # elif response == 2:
                #     self.timer.increase_limit(title)
