from .main import ScreentimeQt
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from .stapplicationcontext import STApplicationContext
from pathlib import Path
import os

MAX_RESULTS = 1000

MODULE_NAME = 'screentime'
HOME = Path(os.environ['HOME'])
home_dir = Path(HOME / '.config' / MODULE_NAME)
config_path = home_dir / 'config.yml'

def run():
    appctxt = STApplicationContext(config_path)
    mw = ScreentimeQt(appctxt)
    mw.show()
    # app.exec_()
    appctxt.app.exec_()
