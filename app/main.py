import sys

from app.bootstrap import ApplicationContainer
from infrastructure.logger import get_logger

from gui.viewmodels.main_vm import MainViewModel
from gui.views.main_window import MainWindow


def main():

    container = ApplicationContainer()

    logger = get_logger(__name__)

    try:

        logger.info("Starting application")

        # -----------------------------
        # Services
        # -----------------------------

        pipeline_service = container.get_pipeline_service()

        # -----------------------------
        # ViewModel
        # -----------------------------

        vm = MainViewModel(
            pipeline_service=pipeline_service
        )

        # -----------------------------
        # GUI
        # -----------------------------

        window = MainWindow(vm)

        window.run()

    except Exception as e:

        logger.exception("Fatal application error")

        sys.exit(1)


if __name__ == "__main__":

    main()