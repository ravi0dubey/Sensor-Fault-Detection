import os,sys
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import ClassficationMetricArtifact
from sklearn.metrics import f1_score,precision_score,recall_score


def get_classfication_score(y_true,y_pred) -> ClassficationMetricArtifact:
    try:
        logging.info("Inside classification metric")
        model_f1_score=f1_score(y_true,y_pred,average="binary", pos_label="neg")
        model_precision_score=precision_score(y_true,y_pred,average="binary", pos_label="neg")
        model_recall_score=recall_score(y_true,y_pred,average="binary", pos_label="neg")
        classification_metric = ClassficationMetricArtifact(f1_score= model_f1_score, precision_score= model_precision_score ,recall_score= model_recall_score)
        logging.info("Exiting classification metric")
        return classification_metric
    except Exception as e:
        raise SensorException(e,sys)