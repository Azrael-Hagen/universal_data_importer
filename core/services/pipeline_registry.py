class PipelineRegistry:

    def __init__(self):
        self._pipelines = {}

    def register(self, file_type: str, tap: str):
        self._pipelines[file_type] = tap

    def resolve(self, file_type: str):

        if file_type not in self._pipelines:
            raise ValueError(f"No pipeline for file type: {file_type}")

        return self._pipelines[file_type]