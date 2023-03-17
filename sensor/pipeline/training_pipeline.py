from sensor.entity.config_entity import TrainingPipelineConfig,  DataIngestionConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import DataIngestionArtifact
import sys,os

class TrainPipeline:
    def __init__(self):
        training_pipeline_config= TrainingPipelineConfig()
        self.data_ingestion_config =DataIngestionConfig(training_pipeline_config= training_pipeline_config)
        self.training_pipeline_config= training_pipeline_config

    def start_data_ingestion(self)-> DataIngestionArtifact:
        try:
            logging.info("Starting data ingestion")
            logging.info("Stop data ingestion")
        except Exception as e:
            raise SensorException(e,sys)
    
    def start_data_validation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)
        
    def start_data_transformation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)

    def start_model_trainer(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)
    
    def start_model_evaluation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)
    
    def start_model_push(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)

    def run_pipeline(self):
        try:
           data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
        except Exception as e:
            raise SensorException(e,sys)