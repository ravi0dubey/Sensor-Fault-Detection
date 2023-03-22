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
