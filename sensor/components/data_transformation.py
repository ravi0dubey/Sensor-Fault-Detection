import sys,os
import numpy as np
import pandas as pd
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact
from sensor.entity.config_entity import DataTransformationConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import save_numpy_array_data,save_object
from sklearn.ml.model.estimator import TargetValueMapping



class DataTransformation:
    def __init__(self,data_validation_config:DataValidationConfig,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_config= data_validation_config 
            self.data_transformation_config= data_transformation_config 
            self._schema_config= read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e,sys)