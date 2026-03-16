from core.detectors.file_detector import detect_file_type

class PipelineService:

    def __init__(self, meltano_service):
        self.meltano_service = meltano_service

    def import_file(self, path):

        file_type = detect_file_type(path)

        if file_type == "csv":
            return self.meltano_service.run_pipeline(
                "tap-csv",
                "target-jsonl"
            )