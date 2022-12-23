import os,sys
from Project.logger import logging
from Project.exception import BikeException
from datetime import datetime


DATASET_NAME = "bike.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"



class training_pipeline_input:
    def __init__(self,):
        self.artifact_dir =  os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")

class data_ingestion_input:
    def __init__(self,training_pipeline_input:training_pipeline_input):
        self.training_pipeline_input = training_pipeline_input
        #making the data_ingestion_dir
        self.data_ingestion_dir = os.path.join(self.training_pipeline_input,"data_ingestion")
        #making the data file folder
        self.data_file = os.path.join(self.data_ingestion_dir,"dataset",DATASET_NAME)
        #making the train file folder
        self.train_file = os.path.join(self.data_ingestion_dir,"train_dataset",TRAIN_FILE_NAME)
        #making the test file folder
        self.test_file = os.path.join(self.data_ingestion_dir,"test_dataset",TEST_FILE_NAME)
        self.test_split = 0.3
        self.database_name = "bsp"
        self.collection_name = "bike"
