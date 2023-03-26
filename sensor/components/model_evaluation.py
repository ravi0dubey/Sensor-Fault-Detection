import sys,os
import numpy as np
import pandas as pd

from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import DataValidationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from sensor.entity.config_entity import DataTransformationConfig,ModelTrainerConfig,ModelEvaluationConfig
from sensor.ml.metric.classification_metric import get_classfication_score
from sensor.ml.model.estimator import SensorModel,ModelResolver
from sensor.utils.main_utils import save_object,load_object

class ModelEvaluation:
    def __init__(self,data_validation_artifact:DataValidationArtifact, 
                 model_trainer_artifact:ModelTrainerArtifact,
                 model_evaluation_config:ModelEvaluationConfig):
        """
        : param model_transformation_artifact : Output reference of data Transformation artifact stage
        : param model_trainer_artifact        : Output reference of Model Trainer artifact stage
        : param model_evaluation_config       : configuration for model evaluation
        """
        try:
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_artifact   = model_trainer_artifact
            self.model_evaluation_config  = model_evaluation_config 
        except Exception as e:
            raise SensorException(e,sys)
        
    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
        try:
            model_accepted= True
            valid_train_file_path = self.data_validation_artifact.valid_train_file_path
            valid_test_file_path = self.data_validation_artifact.valid_test_file_path
            # Valid trained and test file dataframe
            train_df = pd.read_csv(valid_train_file_path)
            test_df  = pd.read_csv(valid_test_file_path)
            # Loading trained model
            model_file_path = self.model_trainer_artifact.trained_model_file_path
            model= load_object(file_path=model_file_path)
            
            model_resolver = ModelResolver()
            if model_resolver.is_model_exists():
                model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted=model_accepted,
                                                                    improved_accuracy= None,
                                                                    best_model_path=None,
                                                                    trained_model_path = model_file_path,
                                                                    train_model_metric_artifact= self.model_trainer_artifact.test_metric_artifact,
                                                                    best_model_metric_artifact = None)
                logging.info(f"Model Evaluation artifact {model_evaluation_artifact}")
                return model_evaluation_artifact         


        except Exception as e:
            raise SensorException(e,sys)    


