from fbs_runtime.application_context.PyQt5 import ApplicationContext
from utils.logger import setup_custom_logger


class STApplicationContext(ApplicationContext):
    def __init__(self, db_path, testing):
        super().__init__()
        self.db_path = db_path
        self.testing = testing
        self.logger = setup_custom_logger("Screentime")
