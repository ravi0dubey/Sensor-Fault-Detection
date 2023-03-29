import os,sys
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME


class TargetValueMapping:
    """
    This class convert or transform the Target value which is of category class
    net is mapped as 0
    pos is mapped as 1
    
    """
    def _init__(self):
        self.net : int = 0
        self.pos : int = 1

    def to_dict(self):
        return self.__dict__
    
    def reverse_mapping(self):
        mapping_response = self.to_dict()
        return dict(zip(mapping_response.values(),mapping_response.keys()))
    

# Class Sensor model has both preprocessor object as well as trained model
class SensorModel:
    """
        Load preprocessor object from Transformed artifact and save it together with our Trained model 
        So that when we need to do prediction, Preprocessor object will be used for data transformation
        while trained model will be used to predict the value using the predict function
    """
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise e
        
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise e
        

 # Class Model Resolver gets the model path and fetches the latest model stored over there       
class ModelResolver:
    def __init__(self,model_dir=SAVED_MODEL_DIR):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise SensorException(e,sys)
        
    def get_best_model_path(self,)-> str:
        try:
            timestamps= list(map(int,os.listdir(self.model_dir)))
            logging.info(f"timestamps : {timestamps}")
            latest_timestamp = max(timestamps)
            logging.info(f"latest_timestamp : {latest_timestamp}")
            latest_model_path = os.path.join(self.model_dir,f"{latest_timestamp}",MODEL_FILE_NAME)
            logging.info(f"latest_model_path : {latest_model_path}")
            return latest_model_path
        except Exception as e:
            raise SensorException(e,sys)
    
    """
    To verify if saved_model folder exists and then we check if timestamp folder exists 
    and then within timestamp folder does model exists in it
    """
    def is_model_exists(self) -> bool:
        try:
            if not os.path.exists(self.model_dir):
                logging.info("Path does not exists")
                return False
            timestamps = os.listdir(self.model_dir)
            if len(timestamps)==0:
                logging.info("Inside timestamps is zero")
                return False          
            latest_model_path= self.get_best_model_path()
            if not os.path.exists(latest_model_path):
                logging.info("Latest model Path does not exists")
                return False
            return True
        except Exception as e:
            raise SensorException(e,sys)