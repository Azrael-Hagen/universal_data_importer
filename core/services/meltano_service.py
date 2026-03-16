from typing import Generator, List
from infrastructure.meltano_runner import MeltanoRunner


class MeltanoService:
    """
    High-level service for interacting with Meltano.

    This service wraps MeltanoRunner and provides a clean API
    for the rest of the application.
    """

    def __init__(self, config):
        self.config = config
        self.runner = MeltanoRunner()

    # ------------------------------------------------
    # Environment
    # ------------------------------------------------

    def check_meltano(self) -> str:
        """
        Verify Meltano is installed and return version.
        """

        output = self.runner.run_and_collect(["meltano", "--version"])
        return output.strip()

    # ------------------------------------------------
    # Plugins
    # ------------------------------------------------

    def list_plugins(self) -> str:
        """
        List installed Meltano plugins.
        """

        return self.runner.run_and_collect(
            ["meltano", "list"]
        )

    def install_plugin(self, plugin_type: str, name: str) -> Generator[str, None, None]:
        """
        Install a Meltano plugin.

        Example:
            install_plugin("extractor", "tap-csv")
        """

        command = [
            "meltano",
            "add",
            plugin_type,
            name
        ]

        yield from self.runner.run(command)

    # ------------------------------------------------
    # Discovery
    # ------------------------------------------------

    def discover_catalog(self, tap: str) -> str:
        """
        Discover catalog for a tap.
        """

        return self.runner.run_and_collect(
            [
                "meltano",
                "invoke",
                tap,
                "--discover"
            ]
        )

    # ------------------------------------------------
    # Pipelines
    # ------------------------------------------------

    def run_pipeline(
        self,
        tap: str,
        target: str
    ) -> Generator[str, None, None]:
        """
        Run a Meltano pipeline.

        Example:
            run_pipeline("tap-csv", "target-jsonl")
        """

        command: List[str] = [
            "meltano",
            "run",
            tap,
            target
        ]

        yield from self.runner.run(command)

    # ------------------------------------------------
    # Utility
    # ------------------------------------------------

    def invoke(self, args: List[str]) -> Generator[str, None, None]:
        """
        Run any Meltano command.

        Example:
            invoke(["meltano", "install"])
        """

        yield from self.runner.run(args)