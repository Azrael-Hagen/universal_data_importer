from abc import ABC, abstractmethod
from typing import Generator

from core.models.pipeline import Pipeline


class PipelineExecutor(ABC):
    """
    Abstract interface for executing pipelines.
    """

    @abstractmethod
    def run_pipeline(self, pipeline: Pipeline) -> Generator[str, None, None]:
        """
        Execute the given pipeline.
        """
        pass