import sys,os
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.entity.config_entity import TrainingPipelineConfig,  DataIngestionConfig
from sensor.data_access.sensor_data import SensorData
from sklearn.model_selection import train_test_split
from pandas import DataFrame


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=   data_ingestion_config  
        except Exception as e:
            raise SensorException(e,sys)
    

    
    def export_data_into_feature_store(self) -> DataFrame:
        """
        Export Mongodb collection record as dataframe into feature store
        get the collection name, feature store file path from data_ingestion_config
        we do not need database name as we have already declared in constant -> database.py
        """       
        try:
            logging.info("Exporting data from mongodb to feature store")
            sensor_data = SensorData()
            dataframe = sensor_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            feature_store_file_path =self.data_ingestion_config.feature_store_file_path
            # creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok= True)
            dataframe.to_csv(feature_store_file_path,index= False, header= True)
            return dataframe
            logging.info("Ending the export of data from mongodb to feature store")
        except Exception as e:
            raise SensorException(e,sys)
    
    def split_data_as_train_test(self,dataframe:DataFrame) -> None:
        # Split the FeatureStore dataset into train and test file using train_test_split_ratio 
        try:
            logging.info("Inside train_test split function")
            train_set,test_set = train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed split of sensor data into train and test")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)      
            os.makedirs(dir_path,exist_ok= True)
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)
            logging.info("storing split of train and test data into train and test folder")
            logging.info("exiting split_data_as_train_test of DataIngestion class")
        except Exception as e:
            raise SensorException(e,sys)


        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            dataframe = self.export_data_into_feature_store()
            self.split_data_as_train_test(dataframe=dataframe)
            print(self.data_ingestion_config.training_file_path)
            print(self.data_ingestion_config.testing_file_path)
            data_ingestion_artifact= DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,test_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact

        except Exception as e:
            raise SensorException(e,sys)  