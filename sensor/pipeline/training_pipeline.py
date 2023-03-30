from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact,ModelPusherArtifact
from sensor.entity.config_entity import TrainingPipelineConfig,  DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig,ModelEvaluationConfig,ModelPusherConfig
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.model_pusher import ModelPusher
from sensor.cloud_storage.s3_syncer import S3Sync
from sensor.constant.s3_bucket import TRAINING_BUCKET_NAME,PREDICTION_BUCKET_NAME
from sensor.constant.training_pipeline import SAVED_MODEL_DIR

import sys,os

class TrainPipeline:
    is_pipeline_running = False
    def __init__(self):
        training_pipeline_config= TrainingPipelineConfig()
        self.data_ingestion_config =DataIngestionConfig(training_pipeline_config= training_pipeline_config)       
        self.training_pipeline_config= training_pipeline_config
        self.s3_sync = S3Sync()


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
            data_validation = DataValidation(data_ingestion_artifact = data_ingestion_artifact,
                                             data_validation_config=self.data_validation_config,)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data Validation completed and artifact: {data_validation_artifact}")
            return data_validation_artifact     
        except Exception as e:
            raise SensorException(e,sys)
        
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact,)-> DataTransformationArtifact:
        try:
            logging.info("Data Transformation started")    
            self.data_transformation_config =DataTransformationConfig(training_pipeline_config= self.training_pipeline_config)      
            data_transformation = DataTransformation(data_validation_artifact = data_validation_artifact,
                                                     data_transformation_config=self.data_transformation_config,)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"Data Transformation complete and artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e,sys)

    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact,)->ModelTrainerArtifact:
        try:
            logging.info("Model Training started") 
            self.model_trainer_config= ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                         model_trainer_config=self.model_trainer_config)
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            logging.info(f"Model Training Complete and artifact : {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e,sys)
    
    def start_model_evaluation(self,data_validation_artifact:DataValidationArtifact,model_trainer_artifact:ModelTrainerArtifact) -> ModelEvaluationArtifact:
        try:
            logging.info("Model Evaluation started") 
            self.model_evaluation_config = ModelEvaluationConfig(training_pipeline_config=self.training_pipeline_config)
            model_evaluation = ModelEvaluation(data_validation_artifact= data_validation_artifact,
                                               model_trainer_artifact=model_trainer_artifact,
                                               model_evaluation_config=self.model_evaluation_config)
            model_evaluation_artifact= model_evaluation.initiate_model_evaluation()
            logging.info(f"Model Evaluation complete and artifact :{model_evaluation_artifact}") 
            return model_evaluation_artifact
        except Exception as e:
            raise SensorException(e,sys)
    
    def start_model_push(self,model_evaluation_artifact:ModelEvaluationArtifact)->ModelPusherArtifact:
        try:
            logging.info("Model Pusher Started")
            self.model_pusher_config =ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)
            model_pusher = ModelPusher(model_evaluation_artifact=model_evaluation_artifact,model_pusher_config = self.model_pusher_config)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            logging.info(f"Model Pushing complete and artifact:{model_pusher_artifact} ")
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e,sys)
    
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.artifact_dir,aws_buket_url=aws_bucket_url)
        except Exception as e:
            raise SensorException(e,sys)
            
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/{SAVED_MODEL_DIR}"
            self.s3_sync.sync_folder_to_s3(folder = SAVED_MODEL_DIR,aws_buket_url=aws_bucket_url)
        except Exception as e:
            raise SensorException(e,sys)

    def run_pipeline(self):
        try:
           TrainPipeline.is_pipeline_running = True

           data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
           data_validation_artifact:DataValidationArtifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
           data_transformation_artifact:DataTransformationArtifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
           model_trainer_artifact:ModelTrainerArtifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
           model_evaluation_artifact:ModelEvaluationArtifact= self.start_model_evaluation(data_validation_artifact=data_validation_artifact,model_trainer_artifact=model_trainer_artifact)
           if not model_evaluation_artifact.is_model_accepted:
               raise Exception("Trained model is not better than the best model")
           model_pusher_artifact:ModelPusherArtifact = self.start_model_push(model_evaluation_artifact=model_evaluation_artifact)
           TrainPipeline.is_pipeline_running = False  
           self.sync_artifact_dir_to_s3()
           self.sync_saved_model_dir_to_s3()
        except Exception as e:
            self.sync_artifact_dir_to_s3()
            TrainPipeline.is_pipeline_running = False  
            raise SensorException(e,sys)
    
    # def run_pipeline(self):
    #     try:
    #         TrainPipeline.is_pipeline_running=True
    #         data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
    #         data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
    #         data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
    #         logging.info(f"Data Transformation inside training pipeline and artifact: {data_transformation_artifact}")
    #         model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
    #         model_eval_artifact = self.start_model_evaluation( model_trainer_artifact, data_validation_artifact)
    #         if not model_eval_artifact.is_model_accepted:
    #             raise Exception("Trained model is not better than the best model")
    #         model_pusher_artifact = self.start_model_pusher(model_eval_artifact)
    #         TrainPipeline.is_pipeline_running=False
    #     except  Exception as e:
    #         TrainPipeline.is_pipeline_running=False
    #         raise  SensorException(e,sys)