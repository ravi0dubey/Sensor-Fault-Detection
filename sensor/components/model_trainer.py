import sys,os
import numpy as np
import pandas as pd
from sensor.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
from sensor.entity.config_entity import DataTransformationConfig,ModelTrainerConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import load_numpy_array_data
from sklearn.model_selection import train_test_split


class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,model_trainer_config:ModelTrainerConfig):
        """
        : param data_Transformation_artifact : Output reference of data Transformation artifact stage
        : param model_trainer_config : configuration for model trainer
        """
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config= model_trainer_config 
        except Exception as e:
            raise SensorException(e,sys)

    def initiate_model_trainer(self)-> ModelTrainerArtifact:
        try:
            # loading Training and Test array
            train_arr= load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)
            test_arr= load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)
            x_train,y_train,x_test,y_test=(
                train_arr[::-1],
                train_arr[:-1],
                test_arr[::-1],
                test_arr[:-1]
            )
        except Exception as e:
            raise SensorException(e,sys)
