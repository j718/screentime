from .main import ScreentimeQt
from fbs_runtime.application_context.PyQt5 import ApplicationContext

def run():
    appctxt = ApplicationContext()
    mw = ScreentimeQt(appctxt)
    mw.show()
    # app.exec_()
    appctxt.app.exec_()
