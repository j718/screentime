from fbs_runtime.application_context.PyQt5 import ApplicationContext
from utils.logger import setup_custom_logger
import threading


class STApplicationContext(ApplicationContext):
    def __init__(self, db_path, testing):
        super().__init__()
        self._lock = threading.Lock()
        self.db_path = db_path
        self.testing = testing
        self.logger = setup_custom_logger("Screentime")
        self.config = None

    def get_config(self):
        with self._lock:
            return self.config

    def set_config(self, config):
        with self._lock:
            self.config = config
