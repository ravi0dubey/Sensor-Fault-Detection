# It will store all the artifacts(output) of each stages/components(data ingestion, data validations, model_training, model_evaluation, model_deployment)
from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str

@dataclass
class DataTransformationArtifact:
    transformed_object_file_path : str
    transformed_train_file_path : str
    transformed_test_file_path : str
    
@dataclass
class ClassficationMetricArtifact:
    f1_score: float
    precision_score: float
    recall_score: float

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    train_metric_artifact: ClassficationMetricArtifact
    test_metric_artifact: ClassficationMetricArtifact

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool
    improved_accuracy: float
    best_model_path: str
    trained_model_path: str
    train_model_metric_artifact: ClassficationMetricArtifact
    best_model_metric_artifact: ClassficationMetricArtifact

@dataclass
class ModelPusherArtifact:
    saved_model_path: str
    model_file_path: str