from abc import ABC, abstractmethod

from core.models.pipeline import Pipeline


class PipelineExecutor(ABC):
    """
    Abstract interface for executing pipelines.
    """

    @abstractmethod
    def run_pipeline(self, pipeline: Pipeline):
        """
        Execute the given pipeline.
        """
        pass