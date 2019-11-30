from .main import ScreentimeQt
from utils.stapplicationcontext import STApplicationContext
from pathlib import Path
import os

MAX_RESULTS = 1000
TESTING = os.environ.get("ST_TESTING", default=False) == 'TRUE'
MODULE_NAME = 'screentime'
HOME = Path(os.environ['HOME'])
if TESTING:
    aqt_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    home_dir = aqt_dir.parent.parent.parent.parent / 'test_data'
    if not home_dir.exists():
        home_dir.mkdir()
else:
    home_dir = Path(HOME / '.local/share' / MODULE_NAME)
config_path = home_dir / 'data.sql'


def run():
    appctxt = STApplicationContext(config_path, TESTING)
    mw = ScreentimeQt(appctxt)
    mw.show()
    # app.exec_()
    appctxt.app.exec_()
