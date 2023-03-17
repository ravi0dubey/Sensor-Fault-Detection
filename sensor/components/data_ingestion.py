import sys,os
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.entity.config_entity import TrainingPipelineConfig,  DataIngestionConfig
from sensor.data_access.sensor_data import SensorData
from pandas import DataFrame


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=   data_ingestion_config  
        except Exception as e:
            raise SensorException(e,sys)
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            pass
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
        pass

        
