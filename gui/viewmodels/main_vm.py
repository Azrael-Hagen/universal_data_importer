class MainViewModel:

    def __init__(self, pipeline_service):
        self.pipeline_service = pipeline_service

    def import_file(self, path):
        return self.pipeline_service.import_file(path)