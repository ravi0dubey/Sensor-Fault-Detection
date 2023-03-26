import sys,os
import numpy as np
import pandas as pd

from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from sensor.entity.config_entity import DataTransformationConfig,ModelTrainerConfig,ModelEvaluationConfig
from sensor.ml.metric.classification_metric import get_classfication_score
from sensor.ml.model.estimator import SensorModel
from sensor.utils.main_utils import save_object,load_object

class ModelEvaluation:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact, 
                 model_trainer_artifact:ModelTrainerArtifact,
                 model_evaluation_config:ModelEvaluationConfig):
        """
        : param model_transformation_artifact : Output reference of data Transformation artifact stage
        : param model_trainer_artifact        : Output reference of Model Trainer artifact stage
        : param model_evaluation_config       : configuration for model evaluation
        """
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_evaluation_config= model_evaluation_config 
        except Exception as e:
            raise SensorException(e,sys)
        

class ModelResolver:
    def __init__(self,model_dir):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise SensorException(e,sys)
        
    def get_best_model(self,)-> str:
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)

