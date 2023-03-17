# It will store all the artifacts(output) of each stages/components(data ingestion, data validations, model_training, model_evaluation, model_deployment)
from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str