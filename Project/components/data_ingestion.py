import os,sys
from Project.logger import logging
from Project.exception import BikeException
from Project.entity.input import data_ingestion_input
import pandas as pd
from Project import utils
from sklearn.model_selection import train_test_split
from Project.entity import output

class DataIngestion:
    def __init__(self,data_ingestion_input:data_ingestion_input):
        try:
            logging.info(f"{'--'*20} DATA INGESTION {'--'*20}")
            self.data_ingestion_input = data_ingestion_input
        except Exception as e:
            print(BikeException(e, error_detail = sys))


    def start_data_ingestion(self,):
        try:
            logging.info("getting the database and collection name")
            #getting the database and collection name
            database  = self.data_ingestion_input.database_name
            collection = self.data_ingestion_input.collection_name
            logging.info("getiing the data in pd.DataFrame")
            #getiing the data in pd.DataFrame 
            df:pd.DataFrame = utils.load_data_from_db(database, collection)

            logging.info("saving the data in dataset folder")
            #saving the data in dataset folder 
            dataset_dir = os.path.dirname(self.data_ingestion_input.data_file)
            logging.info("making the folder if not exist")
            #making the folder if not exist
            os.makedirs(dataset_dir,exist_ok=True)

            logging.info("saving the dataset in csv")
            #saving the dataset in csv
            df.to_csv(path_or_buf=self.data_ingestion_input.data_file,index=False,header=True)

            logging.info("Splliting the data into train and test file")
            #Splliting the data into train and test file 
            train_df,test_df = train_test_split(df,test_size=self.data_ingestion_input.test_split)

            logging.info("making the train file dir name ")
            #making the train file dir name 
            train_dir = os.path.dirname(self.data_ingestion_input.train_file)
            #making the folder if not exist
            os.makedirs(train_dir,exist_ok=True)
            #saving the train dataset in csv
            train_df.to_csv(path_or_buf=self.data_ingestion_input.train_file,index=False,header=True)

            logging.info("making the test file dir name ")
            #making the test file dir name 
            test_dir = os.path.dirname(self.data_ingestion_input.test_file)
            #making the folder if not exist
            os.makedirs(test_dir,exist_ok=True)
            #saving the train dataset in csv
            train_df.to_csv(path_or_buf=self.data_ingestion_input.test_file,index=False,header=True)

            logging.info("making the output of data ingestion")
            #making the output of data ingestion
            data_ingestion_output = output.data_ingestion_output(dataset_file_path=self.data_ingestion_input.data_file,
                                                                 train_file_path = self.data_ingestion_input.train_file, 
                                                                 test_file_path = self.data_ingestion_input.test_file)
            logging.info(f"Output of data ingestion : {data_ingestion_output}")
            
            return data_ingestion_output

        except Exception as e:
            print(BikeException(e, error_detail = sys)) 
