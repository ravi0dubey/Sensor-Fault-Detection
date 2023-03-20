from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.entity.config_entity import TrainingPipelineConfig,  DataIngestionConfig,DataValidationConfig
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
import sys,os

class TrainPipeline:
    def __init__(self):
        training_pipeline_config= TrainingPipelineConfig()
        self.data_ingestion_config =DataIngestionConfig(training_pipeline_config= training_pipeline_config)
        
        self.training_pipeline_config= training_pipeline_config

    def start_data_ingestion(self)-> DataIngestionArtifact:
        try:
            logging.info("Data ingestion Started")
            data_ingestion = DataIngestion(data_ingestion_config = self.data_ingestion_config)
            data_ingestion_artifact= data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e,sys)
    
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact,)-> DataValidationArtifact:
        try:
            logging.info("Data Validation started")      
            self.data_validation_config =DataValidationConfig(training_pipeline_config= self.training_pipeline_config)    
            data_validation = DataValidation(data_ingestion_artifact = data_ingestion_artifact,data_validation_config=self.data_validation_config,)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data Validation completed and artifact: {data_validation_artifact}")
            return data_ingestion_artifact
        
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
           data_validation_artifact:DataValidationArtifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise SensorException(e,sys)