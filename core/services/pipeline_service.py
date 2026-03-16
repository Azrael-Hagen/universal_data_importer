from pathlib import Path
from typing import Generator

from core.detectors.file_detector import detect_file_type
from core.models.datasource import DataSource
from core.models.pipeline import Pipeline


class PipelineService:
    """
    High-level service responsible for building and executing pipelines.
    """

    # Mapping between file types and Meltano taps
    PIPELINE_MAP = {
        "csv": "tap-csv",
        "excel": "tap-excel",
        "json": "tap-json",
    }

    DEFAULT_TARGET = "target-jsonl"

    def __init__(self, meltano_service):
        self.meltano = meltano_service

    # -----------------------------------------
    # Public API
    # -----------------------------------------

    def import_file(self, path: str) -> Generator[str, None, None]:
        """
        Import a file into the pipeline system.
        """

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

        file_type = detect_file_type(path)

        if file_type == "unknown":
            raise ValueError(f"Unsupported file type: {path}")

        return DataSource(path, file_type)

    def _resolve_pipeline(self, datasource: DataSource) -> Pipeline:
        """
        Resolve pipeline configuration for datasource.
        """

        file_type = datasource.file_type

        if file_type not in self.PIPELINE_MAP:
            raise ValueError(f"No pipeline configured for: {file_type}")

        tap = self.PIPELINE_MAP[file_type]

        return Pipeline(tap, self.DEFAULT_TARGET)

    # -----------------------------------------
    # Execution
    # -----------------------------------------

    def _execute_pipeline(self, pipeline: Pipeline) -> Generator[str, None, None]:
        """
        Execute pipeline using Meltano.
        """

        yield from self.meltano.run_pipeline(
            pipeline.source,
            pipeline.target
        )

    # -----------------------------------------
    # Extensibility
    # -----------------------------------------

    def register_pipeline(self, file_type: str, tap: str):
        """
        Register a new pipeline mapping.
        """

        self.PIPELINE_MAP[file_type] = tap