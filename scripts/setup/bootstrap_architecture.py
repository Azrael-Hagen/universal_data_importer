import os
from pathlib import Path

ROOT = Path.cwd()

FILES = {
    "app/main.py": """
from app.bootstrap import create_application

def main():
    app = create_application()
    app.run()

if __name__ == "__main__":
    main()
""",

    "app/bootstrap.py": """
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
""",

    "infrastructure/logger.py": """
import logging

def get_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    return logging.getLogger("UDI")
""",

    "infrastructure/config_manager.py": """
class ConfigManager:

    def __init__(self):
        self.config = {}

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
""",

    "infrastructure/meltano_runner.py": """
import subprocess

class MeltanoRunner:

    def run(self, command):
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        for line in process.stdout:
            yield line.strip()
""",

    "core/services/meltano_service.py": """
from infrastructure.meltano_runner import MeltanoRunner

class MeltanoService:

    def __init__(self, config):
        self.runner = MeltanoRunner()
        self.config = config

    def run_pipeline(self, source, target):
        cmd = ["meltano", "run", source, target]

        for line in self.runner.run(cmd):
            yield line
""",

    "core/services/pipeline_service.py": """
from core.detectors.file_detector import detect_file_type

class PipelineService:

    def __init__(self, meltano_service):
        self.meltano_service = meltano_service

    def import_file(self, path):

        file_type = detect_file_type(path)

        if file_type == "csv":
            return self.meltano_service.run_pipeline(
                "tap-csv",
                "target-jsonl"
            )
""",

    "core/detectors/file_detector.py": """
from pathlib import Path

def detect_file_type(path):

    ext = Path(path).suffix.lower()

    if ext == ".csv":
        return "csv"

    if ext in [".xlsx", ".xls"]:
        return "excel"

    if ext == ".json":
        return "json"

    return "unknown"
""",

    "core/models/pipeline.py": """
class Pipeline:

    def __init__(self, source, target):
        self.source = source
        self.target = target
""",

    "core/models/datasource.py": """
class DataSource:

    def __init__(self, path, file_type):
        self.path = path
        self.file_type = file_type
""",

    "gui/viewmodels/main_vm.py": """
class MainViewModel:

    def __init__(self, pipeline_service):
        self.pipeline_service = pipeline_service

    def import_file(self, path):
        return self.pipeline_service.import_file(path)
""",

    "gui/views/main_window.py": """
class MainWindow:

    def __init__(self, view_model):
        self.vm = view_model

    def start(self):
        print("Universal Data Importer started")
"""
}

def create_file(path, content):

    file_path = ROOT / path
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if not file_path.exists():
        file_path.write_text(content.strip())
        print(f"✔ created {path}")
    else:
        print(f"• skipped {path}")


def main():

    print("\\n=== BOOTSTRAP ARCHITECTURE ===\\n")

    for path, content in FILES.items():
        create_file(path, content)

    print("\\nArchitecture ready.\\n")


if __name__ == "__main__":
    main()