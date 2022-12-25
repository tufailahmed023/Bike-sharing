import os,sys
from Project.logger import logging
from Project.exception import BikeException
from datetime import datetime


DATASET_NAME = "bike.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
REPORT_NAME = "report.ymal"
TRANSFORMER_NAME = "transformer.pkl"
MODEL_NAME = "model.pkl"
ACCURACY_REPORT_NAME  = "accuracy.ymal"

class training_pipeline_input:
    def __init__(self,):
        self.artifact_dir =  os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")

class data_ingestion_input:
    def __init__(self,training_pipeline_input:training_pipeline_input):
        self.training_pipeline_input = training_pipeline_input
        #making the data_ingestion_dir
        self.data_ingestion_dir = os.path.join(self.training_pipeline_input.artifact_dir,"data_ingestion")
        #making the data file folder
        self.data_file = os.path.join(self.data_ingestion_dir,"dataset",DATASET_NAME)
        #making the train file folder
        self.train_file = os.path.join(self.data_ingestion_dir,"train_dataset",TRAIN_FILE_NAME)
        #making the test file folder
        self.test_file = os.path.join(self.data_ingestion_dir,"test_dataset",TEST_FILE_NAME)
        self.test_split = 0.3
        self.database_name = "bsp"
        self.collection_name = "bike"


class data_validation_input:
    def __init__(self,training_pipeline_input:training_pipeline_input):
        self.training_pipeline_input = training_pipeline_input
        self.data_validation_dir = os.path.join(self.training_pipeline_input.artifact_dir,"data_validation")
        self.report  = os.path.join(self.data_validation_dir,REPORT_NAME)
        self.base_dataframe_path = os.path.join("day.csv")


class data_tranformation_input:
    def __init__(self,training_pipeline_input:training_pipeline_input):
        self.training_pipeline_input = training_pipeline_input
        self.data_tranformation_dir = os.path.join(self.training_pipeline_input.artifact_dir,"data_tranformation")
        self.tranformer_path = os.path.join(self.data_tranformation_dir,"transformer",TRANSFORMER_NAME)
        self.tranfomed_train_data = os.path.join(self.data_tranformation_dir,"tranfomed_train_data",TRAIN_FILE_NAME)
        self.tranfomed_test_data = os.path.join(self.data_tranformation_dir,"tranfomed_test_data",TEST_FILE_NAME)


class model_training_input:
    def __init__(self,training_pipeline_input:training_pipeline_input):
        self.training_pipeline_input = training_pipeline_input
        self.model_training_dir = os.path.join(self.training_pipeline_input.artifact_dir,"model_training")
        self.model_file_path =  os.path.join(self.model_training_dir,"model",MODEL_NAME)
        self.accuracy_report_path = os.path.join(self.model_training_dir,"accuracy",ACCURACY_REPORT_NAME)


class model_evaluatiion_input:
    def __init__(self,training_pipeline_input:training_pipeline_input):
        self.training_pipeline_input = training_pipeline_input
        self.change_accuracy_thresholde = 0.01


class model_pusher_input:
    def __init__(self,training_pipeline_input:training_pipeline_input):
        self.Saved_models_dir = os.path.join("Saved_models")
