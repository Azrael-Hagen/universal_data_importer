from infrastructure.logger import get_logger
from infrastructure.config_manager import ConfigManager
from core.services.meltano_service import MeltanoService
from core.services.pipeline_service import PipelineService
from gui.viewmodels.main_vm import MainViewModel
from gui.views.main_window import MainWindow

class Application:

    def __init__(self):
        self.logger = get_logger()
        self.config = ConfigManager()
        self.meltano_service = MeltanoService(self.config)
        self.pipeline_service = PipelineService(self.meltano_service)

    def run(self):
        vm = MainViewModel(self.pipeline_service)
        window = MainWindow(vm)
        window.start()


def create_application():
    return Application()