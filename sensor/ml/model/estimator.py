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