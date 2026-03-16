import subprocess
from typing import List, Generator


class MeltanoRunner:
    """
    Low-level interface for executing Meltano CLI commands.

    This class is responsible for:
    - Executing Meltano commands
    - Streaming output
    - Handling process errors
    """

    def run(self, command: List[str]) -> Generator[str, None, int]:
        """
        Execute a command and stream its output.

        Args:
            command: Command list (e.g. ["meltano", "run", "tap-csv", "target-jsonl"])

        Yields:
            Output lines from the process
        """

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # Stream stdout
        for line in process.stdout:
            yield line.rstrip()

        # Wait for process completion
        process.wait()

        # If error occurred, stream stderr
        if process.returncode != 0:
            error_output = process.stderr.read()
            raise RuntimeError(
                f"Meltano command failed ({process.returncode}):\n{error_output}"
            )

        return process.returncode

    def run_and_collect(self, command: List[str]) -> str:
        """
        Execute command and return full output.

        Useful for commands where streaming is not required.
        """

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        return result.stdout

    def run_pipeline(self, tap: str, target: str):
        """
        Convenience method for running pipelines.
        """

        command = [
            "meltano",
            "run",
            tap,
            target
        ]

        return self.run(command)