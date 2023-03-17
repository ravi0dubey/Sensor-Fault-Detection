from sensor.configuration.mongo_db_connection import   MongoDBClient
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import TrainingPipelineConfig,  DataIngestionConfig
import os,sys

if __name__=='__main__':
    mongodb_client = MongoDBClient()
    print("collection names: " ,mongodb_client.database.list_collection_names())
    training_pipeline_config= TrainingPipelineConfig()
    data_ingestion_config =DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    print(data_ingestion_config.__dict__)

    
    