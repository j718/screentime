
from PyQt5.QtCore import pyqtSlot, QRunnable
from screentime.timer import Screentime
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
        self.timer = Screentime()

    @pyqtSlot()
    def run(self):
        while True:
            self.block_apps()
            time.sleep(5)

    def block_apps(self):
        """ closes blocked apps """
        blocked = self.timer.apply_limits()
        app_list = str(subprocess.check_output(['wmctrl', '-l']))
        for index, app in blocked.iterrows():
            if app.id.lower() in app_list.lower():
                self.closer.set_warning(app.id, app.limit)
                print(f"Sending warning for {app.id}")
                response = self.closer.exec_()
                if response == 1:
                    print(f"Killed {app.id}")
                    subprocess.call(['notify-send',
                                    f'Closing {app.id}. Time limit reached.'])
                    subprocess.Popen(["wmctrl", "-c", app.id], bufsize=0)
                elif response == 2:
                    self.timer.increase_limit(app.id)
