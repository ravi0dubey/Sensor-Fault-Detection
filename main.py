from sensor.configuration.mongo_db_connection import   MongoDBClient
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import TrainingPipelineConfig,  DataIngestionConfig
from sensor.pipeline.training_pipeline import TrainPipeline
import os,sys

if __name__=='__main__':
    try:
    # mongodb_client = MongoDBClient()
    # print("collection names: " ,mongodb_client.database.list_collection_names())
    # training_pipeline_config= TrainingPipelineConfig()
    # data_ingestion_config =DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    # print(data_ingestion_config.__dict__)
        training_pipeline=TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)

    
    