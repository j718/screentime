from fbs_runtime.application_context.PyQt5 import ApplicationContext


class STApplicationContext(ApplicationContext):
    def __init__(self, db_path, testing):
        super().__init__()
        self.db_path = db_path
        self.testing = testing
