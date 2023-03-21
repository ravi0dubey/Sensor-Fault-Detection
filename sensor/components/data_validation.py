import sys,os
from scipy import stats
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import read_yaml_file,write_yaml_file
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
            number_of_columns = len(self._schema_config["columns"])
            logging.info(f"number of columns is {number_of_columns}")
            number_of_df_columns= len(dataframe.columns)
            logging.info(f"number of dataframe column is {number_of_df_columns}")
            if number_of_columns==number_of_df_columns:
                return True
            else:
                return False
        except Exception as e:
            raise SensorException(e,sys)
    
    
    # def is_numerical_column_exist(self,dataframe: pd.DataFrame) -> bool:
    #     try:
    #         missing_numerical_columns = []
    #         numerical_columns = self._schema_config["numerical_columns"]
    #         numerical_columns_present = True
    #         for columns in numerical_columns:
    #             if columns not in dataframe.columns:
    #                 numerical_columns_present = False
    #                 missing_numerical_columns.append(columns)            
    #         logging.info(f"Missing numerical columns : [{missing_numerical_columns}]")    
    #         return numerical_columns_present
    #     except Exception as e:
    #         raise SensorException(e,sys)
    
    def is_numerical_column_exist(self,dataframe: pd.DataFrame) -> bool:
       """
       This function check numerical column is present in dataframe or not
       :param df:
       :return: True if all column presents else False
       """
       try:
            missing_numerical_columns = []
            dataframe_columns = dataframe.columns
            status = True
            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    status = False
                    missing_numerical_columns.append(column)
            logging.info(f"Missing numerical column: {missing_numerical_columns}")
            return status
       except Exception as e:
            raise SensorException(e, sys) from e
    
    
    def drop_zero_std_columns(self,dataframe: pd.DataFrame) -> bool:
        pass
   
    @staticmethod
    def read_data(file_path)-> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e,sys)

        
    def detect_dataset_drift(self,base_dataframe: pd.DataFrame,current_dataframe: pd.DataFrame)-> bool:
        try:
            drift_status = True
            report = {}
            for column in base_dataframe.columns:
                d1 = base_dataframe[column]
                d2 = base_dataframe[column]
                is_same_dist = stats.ks_2samp(d1,d2)
                if self.data_validation_config.p_value_threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    drift_status = False
                    report.update({column:{"p_value": float(is_same_dist.pvalue),"drift_status":is_found}})
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path           
            # create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok= True)
            write_yaml_file(file_path=drift_report_file_path,content=report)
            return drift_status
        except Exception as e:
            raise SensorException(e,sys)  


    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            validation_error_message = " "
            train_file_path= self.data_ingestion_artifact.trained_file_path
            test_file_path= self.data_ingestion_artifact.test_file_path

            # Reading data from train and test file location
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            # Validate number of columns
            logging.info("Validating Train dataframe number of columns")
            if not (self.validate_number_of_columns(dataframe= train_dataframe)):
                validation_error_message = "Train Dataframe does not have all columns\n"
            logging.info("Validating Test dataframe number of columns")
            if not(self.validate_number_of_columns(dataframe= test_dataframe)):
                validation_error_message = "Test Dataframe does not have all columns\n"           

            # Validate numerical columns
            logging.info("Validating Train dataframe numerical columns")
            if not (self.is_numerical_column_exist(dataframe= train_dataframe)):
                validation_error_message = "Train Dataframe does not have all numerical columns\n"
            logging.info("Validating Test dataframe numerical columns")
            if not(self.is_numerical_column_exist(dataframe= test_dataframe)):
                validation_error_message = "Test Dataframe does not have all numerical columns\n"  

            if len(validation_error_message) > 1:
                print(f"Validation Error Message {validation_error_message}\n")
                print(f"Length of Validation Error Message {len(validation_error_message)}\n")
                raise Exception(validation_error_message)

            # check data drift
            drift_status = self.detect_dataset_drift(base_dataframe=train_dataframe,current_dataframe=test_dataframe)

            #create data validation artifact
            data_validation_artifact= DataValidationArtifact(
                validation_status=drift_status,
                valid_train_file_path=train_file_path,
                valid_test_file_path=test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_train_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
                  )
            logging.info(f"Data Validation Artifact :{data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise SensorException(e,sys)  