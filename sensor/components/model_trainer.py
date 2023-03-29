import sys,os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from sensor.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
from sensor.entity.config_entity import DataTransformationConfig,ModelTrainerConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import load_numpy_array_data
from sensor.ml.metric.classification_metric import get_classfication_score
from sensor.ml.model.estimator import SensorModel
from sensor.utils.main_utils import save_object,load_object

class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,model_trainer_config:ModelTrainerConfig):
        """
        : param data_Transformation_artifact : Output reference of data Transformation artifact stage
        : param model_trainer_config : configuration for model trainer
        """
        try:
            self.data_transformation_artifact = data_transformation_artifact
            # self.model_trainer_config= model_trainer_config 
            self.model_trainer_config=model_trainer_config
            print(self.model_trainer_config)
        except Exception as e:
            raise SensorException(e,sys)


    # def perform_hyper_parameter_tuning(self,)
    def  train_model(self,x_train,y_train):
        """
        model prediction done on training data
        """
        try:
            logging.info("Inside Model Training")
            xgb_clf= XGBClassifier()
            xgb_clf.fit(x_train,y_train)
            logging.info("Exiting Model Training")
            return xgb_clf
        except Exception as e:
            raise SensorException(e,sys)


    def initiate_model_trainer(self)-> ModelTrainerArtifact:
        try:         
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            print(f"train_file_path : {train_file_path}")
            print(f"test_file_path : {test_file_path}")
            #loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )
            
            # prediction of training and testing data
            print(f"x_train: {x_train}")
            print(f"y_train: {y_train}")
            classification_model = self.train_model(x_train,y_train)
            y_train_pred = classification_model.predict(x_train)
            print(f"y_train_pred: {y_train_pred}")
            classification_train_metric= get_classfication_score(y_true= y_train,y_pred=y_train_pred)
            
            if classification_train_metric.f1_score < self.model_trainer_config.expected_accuracy:
                raise Exception(f"Training Model f1 score is less than threshold decided{self.model_trainer_config.expected_accuracy}")
            
            y_test_pred = classification_model.predict(x_test)
            classification_test_metric = get_classfication_score(y_true= y_test,y_pred= y_test_pred)

            # Calculated the difference of f1 score of Train and Test prediction values to figure out the Underfitting and Overfitting 
            diff_f1_metric =  abs(classification_train_metric.f1_score - classification_test_metric.f1_score)

            if diff_f1_metric > self.model_trainer_config.overfitting_underfitting_threshold:
                raise Exception("Model is not good, try doing more experimentation")
            
            
            """
            Load preprocessor object from Transformed artifact and save it together with our Trained model 
            So that when we need to do prediction, Preprocessor object will be used for data transformation
            while trained model will be used to predict the value using the predict function
            """
            preprocessor_obj = load_object(file_path= self.data_transformation_artifact.transformed_object_file_path)
            model_trained_file_path = self.model_trainer_config.trained_model_file_path
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            print(f"trained_model_file_path:{model_trained_file_path}")
            print(f"model_dir_path: {model_dir_path}")
            os.makedirs(model_dir_path,exist_ok= True)
            sensor_model = SensorModel(preprocessor=preprocessor_obj,model=classification_model)
            print(f"sensor_model: {sensor_model}")
            print(f"model_dir_path: {model_dir_path}")
            save_object(self.model_trainer_config.trained_model_file_path, obj=sensor_model)
            # save_object(file_path=model_dir_path, obj=sensor_model)
            
            # Model Trainer Artifact
            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=model_trained_file_path ,
                                                          train_metric_artifact= classification_train_metric, 
                                                          test_metric_artifact=classification_test_metric)
            logging.info(f"Model Trainer artifact {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e,sys)
