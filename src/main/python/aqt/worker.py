from PyQt5.QtCore import pyqtSlot, QRunnable
from utils.timer import Screentime
import time
import subprocess
from aqt.closer import Closer


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

    @pyqtSlot()
    def run(self):
        while True:
            self.block_apps()
            time.sleep(10)
            # TODO increase increment based on which is closest to rnning out

    def block_apps(self):
        """ closes blocked apps """
        blocked = self.timer.apply_limits()
        app_list = str(subprocess.check_output(['wmctrl', '-l']))
        for index, row in blocked.iterrows():
            if row.app.lower() in app_list.lower():
                self.closer.set_warning(row.title, row.time_limit)
                self.appctxt.logger.info(f"Sending warning for {row.app}")
                response = self.closer.exec_()
                if response == 1:
                    self.appctxt.logger.info(f"Killed {row.app}")
                    subprocess.call(['notify-send',
                                    f'Closing {row.app}. Time limit reached.'])
                    subprocess.Popen(["wmctrl", "-c", row.app], bufsize=0)
                elif response == 2:
                    self.timer.increase_limit(row.app)
