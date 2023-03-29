import sys,os
import shutil
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import ModelTrainerArtifact,ModelEvaluationArtifact,ModelPusherArtifact
from sensor.entity.config_entity import ModelTrainerConfig,ModelEvaluationConfig,ModelPusherConfig
from sensor.ml.metric.classification_metric import get_classfication_score
from sensor.ml.model.estimator import SensorModel,ModelResolver
from sensor.utils.main_utils import save_object,load_object,write_yaml_file

class ModelPusher:
    def __init__(self,model_evaluation_artifact:ModelEvaluationArtifact, 
                 model_pusher_config:ModelPusherConfig):
        """
        : param model_Evaluation_artifact  : Output reference of data Transformation artifact stage
        : param model_pusher_config       : configuration for model pusher
        """
        try:
            self.model_evaluation_artifact = model_evaluation_artifact
            self.model_pusher_config       = model_pusher_config 
        except Exception as e:
            raise SensorException(e,sys)
        
    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            logging.info("Inside Model Pusher initiate")
            trained_model_path = self.model_evaluation_artifact.trained_model_path
            logging.info(f"trained_model_path : {trained_model_path}")

            # creating model pusher dir to save the model
            model_file_path = self.model_pusher_config.model_file_path
            logging.info(f"model_file_path : {model_file_path}")

            os.makedirs(os.path.dirname(model_file_path),exist_ok=True)
            shutil.copy(src= trained_model_path,dst=model_file_path)

            # copy the model in saved model directory
            saved_model_file_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_file_path),exist_ok=True)
            shutil.copy(src= trained_model_path,dst=saved_model_file_path)

            #prepare the artifact
            model_pusher_artifact= ModelPusherArtifact( saved_model_path=saved_model_file_path,model_file_path=model_file_path   )
            logging.info(f"Model Pusher artifact {model_pusher_artifact}")
            return model_pusher_artifact 

        except Exception as e:
            raise SensorException(e,sys)