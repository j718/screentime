from PyQt5.QtCore import pyqtSlot, QRunnable
from utils.timer import Screentime
import time
import subprocess
from aqt.closer import Closer
import signal
import os
import pgrep


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
        self.logger = self.appctxt.logger

    @pyqtSlot()
    def run(self):
        while True:
            self.block_apps()
            time.sleep(10)
            # TODO increase increment based on which is closest to rnning out
            # TODO finish making tray work on startup

    def block_apps(self):
        """ closes blocked apps """
        blocked = self.timer.apply_limits()
        for index, row in blocked.iterrows():
            instance = pgrep.pgrep(row.app)
            if instance:
                self.closer.set_warning(row.app, row.time_limit)
                # self.appctxt.logger.info(f"Sending warning for {row.app}")
                response = self.closer.exec_()
                if response == 1:
                    self.appctxt.logger.info(f"Killed {row.app}")
                    subprocess.call(['notify-send',
                                    f'Closing {row.app}. Time limit reached.'])
                    for pid in instance:
                        os.kill(pid, signal.SIGKILL)
                        # TODO show current progress on usage of a category
