import sys,os
import numpy as np
import pandas as pd
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact
from sensor.entity.config_entity import DataTransformationConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import save_numpy_array_data,save_object
from sensor.ml.model.estimator import TargetValueMapping




class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        """
        : param data_validation_artifact : Output reference of data ingestion artifact stage
        : param data_transformation_config : configuration for data transformation
        """
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config= data_transformation_config 
        except Exception as e:
            raise SensorException(e,sys)
        
        
    @staticmethod
    def read_data(file_path)-> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e,sys)

    @classmethod
    def get_data_transformer_object(cls)-> Pipeline:
        try:
            robut_scaler = RobustScaler()
            simple_imputer= SimpleImputer(strategy="constant",fill_value=0)
            preprocessor = Pipeline(
                steps = [
                ("Imputer",simple_imputer), # replace missing values with zeros
                ("RobustScaler",robut_scaler) #keep every feature in same range and handle outlier
                ]
            )
            return preprocessor
        except Exception as e:
            raise SensorException(e,sys)
        
    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Inside Data Transformation")
            validation_error_message = " "
            train_file_path= self.data_validation_artifact.trained_file_path
            test_file_path= self.data_validation_artifact.test_file_path

            # Reading data from train and test file location
            train_dataframe = DataTransformation.read_data(train_file_path)
            test_dataframe = DataTransformation.read_data(test_file_path)
    

            # Create train input feature df by dropping target column
            input_feature_train_df  = train_dataframe.drop(columns= [TARGET_COLUMN],axis= 1)
            target_feature_train_df = train_dataframe.TARGET_COLUMN
            target_feature_train_df = target_feature_train_df.replace(TargetValueMapping.to_dict())

            # Create test input feature df by dropping target column
            input_feature_test_df  = test_dataframe.drop(columns= [TARGET_COLUMN],axis= 1)
            target_feature_test_df = test_dataframe.TARGET_COLUMN
            target_feature_test_df = target_feature_test_df.replace(TargetValueMapping.to_dict())

            #transformation of Training and Test input feature
            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature= preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature= preprocessor_object.transform(input_feature_test_df)

            #SMOTE for minority classification
            smt = SMOTETomek(sampling_strategy="minority")
            input_feature_train_final,target_feature_train_final = smt.fit_resample(transformed_input_train_feature,target_feature_train_df)
            input_feature_test_final,target_feature_test_final = smt.fit_resample(transformed_input_test_feature,target_feature_test_df)

            # Concatenating the train final and target feature into train_arr
            train_arr = np.c_[input_feature_train_final,np.array(target_feature_train_final)]
            # Concatenating the test final and target feature into test_arr
            test_arr = np.c_[input_feature_test_final,np.array(target_feature_test_final)]

            # save train numpy array data
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            # save test numpy array data
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)

            # save preprocessing object
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor)
            
            # return the artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path =self.data_transformation_config.transformed_test_file_path
            )

        except Exception as e:
            raise SensorException(e,sys)