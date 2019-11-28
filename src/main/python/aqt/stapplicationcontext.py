from fbs_runtime.application_context.PyQt5 import ApplicationContext


class STApplicationContext(ApplicationContext):
    def __init__(self, config_path):
        super().__init__()
        self.config_path = config_path
