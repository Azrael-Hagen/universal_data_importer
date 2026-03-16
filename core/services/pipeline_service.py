from pathlib import Path
from typing import Generator
import time

from core.models.pipeline_result import PipelineResult
from core.detectors.file_detector import detect_file_type
from core.models.datasource import DataSource
from core.models.pipeline import Pipeline
from core.executors.pipeline_executor import PipelineExecutor
from infrastructure.logger import get_logger


class PipelineService:

    """
    High-level service responsible for building and executing pipelines.
    """


    logger = get_logger(__name__)
    
    PIPELINE_MAP: dict[str, str] = {
        "csv": "tap-csv",
        "excel": "tap-excel",
        "json": "tap-json",
    }

    DEFAULT_TARGET = "target-jsonl"

    def __init__(self, executor: PipelineExecutor):

        self.executor = executor
        self.last_result: PipelineResult | None = None

    # -----------------------------------------
    # Public API
    # -----------------------------------------

    def import_file(self, path: str) -> Generator[str, None, None]:

        datasource = self._build_datasource(path)

        pipeline = self._resolve_pipeline(datasource)

        yield from self._execute_pipeline(pipeline)

    # -----------------------------------------
    # Pipeline building
    # -----------------------------------------

    def _build_datasource(self, path: str) -> DataSource:
        """
        Create DataSource model from file.
        """

        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if not file_path.is_file():
            raise ValueError(f"Not a valid file: {path}")

        file_type = detect_file_type(path)

        if file_type == "unknown":
            raise ValueError(f"Unsupported file type: {path}")

        return DataSource(path, file_type)

    def _resolve_pipeline(self, datasource: DataSource) -> Pipeline:

        file_type = datasource.file_type

        if file_type not in self.PIPELINE_MAP:
            raise ValueError(f"No pipeline configured for: {file_type}")

        tap = self.PIPELINE_MAP[file_type]

        return Pipeline(tap, self.DEFAULT_TARGET)

    # -----------------------------------------
    # Execution
    # -----------------------------------------

    def _execute_pipeline(self, pipeline: Pipeline):

        start = time.time()

        try:

            for line in self.executor.run_pipeline(pipeline):
                yield line

            duration = time.time() - start

            self.last_result = PipelineResult(
                success=True,
                execution_time=duration
            )

        except Exception as e:

            duration = time.time() - start

            self.last_result = PipelineResult(
                success=False,
                error=str(e),
                execution_time=duration
            )

            yield f"Pipeline execution failed: {str(e)}"
    # -----------------------------------------
    # Extensibility
    # -----------------------------------------

    def register_pipeline(self, file_type: str, tap: str):

        self.PIPELINE_MAP[file_type] = tap
        self.logger.info(f"Registered pipeline for {file_type} using {tap}")
    
    # -----------------------------------------
    # Accessors
    # -----------------------------------------

    def get_last_result(self) -> PipelineResult | None:
        """
        Return the result of the last executed pipeline.
        """
        return self.last_result