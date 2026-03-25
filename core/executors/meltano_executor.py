from typing import Generator

from core.executors.pipeline_executor import PipelineExecutor
from core.models.pipeline import Pipeline
from infrastructure.meltano_runner import MeltanoRunner


class MeltanoExecutor(PipelineExecutor):
    """
    Executes pipelines using Meltano.
    """

    def __init__(self, config):

        self.runner = MeltanoRunner(config)

    def run_pipeline(self, pipeline: Pipeline) -> Generator[str, None, None]:

        extractor = pipeline.source
        target = pipeline.target

        return self.runner.run(
            extractor=extractor,
            target=target
        )