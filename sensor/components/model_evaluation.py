import sys,os
import numpy as np
import pandas as pd

from sensor.exception import SensorException
from sensor.logger import logging
from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.entity.artifact_entity import DataValidationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from sensor.entity.config_entity import DataTransformationConfig,ModelTrainerConfig,ModelEvaluationConfig
from sensor.ml.metric.classification_metric import get_classfication_score
from sensor.ml.model.estimator import SensorModel,ModelResolver,TargetValueMapping
from sensor.utils.main_utils import save_object,load_object,write_yaml_file


class ModelEvaluation:
    def __init__(self,data_validation_artifact:DataValidationArtifact, 
                 model_trainer_artifact:ModelTrainerArtifact,
                 model_evaluation_config:ModelEvaluationConfig):
        """
        : param model_transformation_artifact : Output reference of data Transformation artifact stage
        : param model_trainer_artifact        : Output reference of Model Trainer artifact stage
        : param model_evaluation_config       : configuration for model evaluation
        """
        try:
            self.data_validation_artifact = data_validation_artifact
            print(f"data_validation_artifact: {data_validation_artifact}")
            data_validation_artifact.valid_train_file_path
            self.model_trainer_artifact   = model_trainer_artifact
            self.model_evaluation_config  = model_evaluation_config 
        except Exception as e:
            raise SensorException(e,sys)
        
    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
        try:
            
            valid_train_file_path = self.data_validation_artifact.valid_train_file_path
            valid_test_file_path = self.data_validation_artifact.valid_test_file_path
            # Valid trained and test file dataframegot
            train_df = pd.read_csv(valid_train_file_path)
            test_df  = pd.read_csv(valid_test_file_path)
            df= pd.concat([train_df,test_df])
            logging.info(f"df[TARGET_COLUMN]: {df[TARGET_COLUMN]}")

            y_true_value = df[TARGET_COLUMN]
            # .replace(TargetValueMapping().to_dict,inplace=True)
            df.drop(TARGET_COLUMN,axis=1,inplace=True)
            # Loading trained model
            train_model_file_path = self.model_trainer_artifact.trained_model_file_path            
            model_resolver = ModelResolver()

            #If model does not exist, i.e this is the first time we are training the model then we will accpet the current model 
            # and exit from this function
            model_accepted= True
            if not model_resolver.is_model_exists():
                model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted=model_accepted,
                                                                    improved_accuracy= None,
                                                                    best_model_path=None,
                                                                    trained_model_path = train_model_file_path,
                                                                    train_model_metric_artifact= self.model_trainer_artifact.test_metric_artifact,
                                                                    best_model_metric_artifact = None)
                logging.info(f"Model does not exist. Model Evaluation artifact {model_evaluation_artifact}")
                return model_evaluation_artifact         
            
            #load Trained model and Latest_model which exist in the saved folder
            train_model = load_object(train_model_file_path)
            latest_model_path= model_resolver.get_best_model_path()
            latest_model = load_object(latest_model_path)
        

            #Determine the predict values for Trained model and Latest model residing in Saved folder
            y_trained_pred = train_model.predict(df)
            y_latest_pred = latest_model.predict(df)
            
            #Determine the metric for Trained model and Latest model
            trained_metric = get_classfication_score(y_true=y_true_value,y_pred=y_trained_pred)
            latest_metric = get_classfication_score(y_true=y_true_value,y_pred=y_latest_pred)

            # If Metric value of Trained model is greater than Latest existing model metric by changed threshold value
            # then we will accept the training model else we will reject it
        
            changed_accuracy = round(latest_metric.f1_score - trained_metric.f1_score,3)
            logging.info(f"trained_metric.f1_score : {trained_metric.f1_score}")
            logging.info(f"latest_metric.f1_score : {latest_metric.f1_score}")
            logging.info(f"changed_accuracy: {changed_accuracy}")
            
            if  changed_accuracy >= self.model_evaluation_config.changed_threshold:
                model_accepted = True
            else:
                model_accepted = False

            model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted=model_accepted,
                                                                    improved_accuracy= changed_accuracy,
                                                                    best_model_path=latest_model_path,
                                                                    trained_model_path = train_model_file_path,
                                                                    train_model_metric_artifact= trained_metric,
                                                                    best_model_metric_artifact = latest_metric)
            logging.info(f"Model Evaluation artifact {model_evaluation_artifact}")
            # save the report
            model_eval_report = model_evaluation_artifact.__dict__
            write_yaml_file(self.model_evaluation_config.report_file_path,model_eval_report)
            return model_evaluation_artifact    

        except Exception as e:
            raise SensorException(e,sys)    


