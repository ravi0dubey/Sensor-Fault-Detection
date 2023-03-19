import sys,os
from scipy import stats
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


    def detect_dataset_drift(self,):
        pass
    


        
    def initiate_data_validation(self,base_dataframe: pd.DataFrame,current_dataframe: pd.DataFrame) -> DataValidationArtifact:
        try:
            report = {}
            for column in base_dataframe.columns:
                d1 = base_dataframe[column]
                d2 = base_dataframe[column]
                is_same_dist = stats.ks_2samp(d1,d2)
                if self.data_validation_config.p_value_threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    report.update({column:{"p_value": float(is_same_dist.pvalue),"drift_status":is_found}})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            # create directory
            dir_path = os.path.dirname(drift_report_file_path)
            
            return report
        except Exception as e:
            raise SensorException(e,sys)  