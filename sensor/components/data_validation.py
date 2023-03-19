import sys,os
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import read_yaml_file
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.artifact_entity import DataValidationArtifact,DataIngestionArtifact
from sensor.entity.config_entity import TrainingPipelineConfig,  DataValidationConfig

from sklearn.model_selection import train_test_split
import pandas as pd


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact, data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact= data_ingestion_artifact
            self.data_validation_config= data_validation_config 
            self._schema_config= read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e,sys)
    
    def validate_number_of_columns(self,dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = self._schema_config["columns"]
            number_of_df_columns= len(dataframe.columns)
            if number_of_columns==number_of_df_columns:
                return True
            else:
                return False
        except Exception as e:
            raise SensorException(e,sys)
    
    def is_numerical_column_exist(self,dataframe: pd.DataFrame) -> bool:
        try:
            missing_numerical_columns = []
            numerical_columns = self._schema_config["numerical_columns"]
            numerical_columns_present = True
            for columns in numerical_columns:
                if columns not in dataframe.columns:
                    numerical_columns_present = False
                    missing_numerical_columns.append(columns)            
            logging.info(f"Missing numerical columns : [{missing_numerical_columns}]")    
            return numerical_columns_present
        except Exception as e:
            raise SensorException(e,sys)
    
    def drop_zero_std_columns(self,dataframe: pd.DataFrame) -> bool:
        pass
   
    @staticmethod
    def read_data(file_path)-> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e,sys)


    def detect_dataset_drift(self):
        pass
    


        
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            error_message = " "
            train_file_path= self.data_ingestion_artifact.trained_file_path
            test_file_path= self.data_ingestion_artifact.test_file_path
            
            # Reading data from train and test file location
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            
            # Validate number of columns
            if not (self.validate_number_of_columns(dataframe== train_dataframe)):
                error_message = "Train Dataframe does not have all columns\n"
            if not(self.validate_number_of_columns(dataframe== test_dataframe)):
                error_message = "Test Dataframe does not have all columns\n"           
            
            # Validate numerical columns
            if not (self.is_numerical_column_exist(dataframe== train_dataframe)):
                error_message = "Train Dataframe does not have all numerical columns\n"
            if not(self.is_numerical_column_exist(dataframe== test_dataframe)):
                error_message = "Test Dataframe does not have all numerical columns\n"  
            
            if len(error_message) > 0:
                raise Exception(error_message)
            
            # check data drift

        except Exception as e:
            raise SensorException(e,sys)  