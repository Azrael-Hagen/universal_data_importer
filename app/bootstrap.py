from infrastructure.config_manager import ConfigManager
from infrastructure.logger import setup_logging, get_logger

from core.services.meltano_service import MeltanoService
from core.services.pipeline_service import PipelineService


class ApplicationContainer:
    """
    Dependency container for the application.
    """

    def __init__(self):

        # -----------------------------
        # Configuration
        # -----------------------------

        self.config = ConfigManager()

        # -----------------------------
        # Logging
        # -----------------------------

        setup_logging(self.config)
        self.logger = get_logger("app")

        self.logger.info("Application bootstrap starting")

        # -----------------------------
        # Services
        # -----------------------------

        self.meltano_service = MeltanoService(self.config)

        self.pipeline_service = PipelineService(
            self.meltano_service
        )

        self.logger.info("Services initialized")

    # ----------------------------------
    # Access helpers
    # ----------------------------------

    def get_config(self):

        return self.config

    def get_pipeline_service(self):

        return self.pipeline_service

    def get_meltano_service(self):

        return self.meltano_service