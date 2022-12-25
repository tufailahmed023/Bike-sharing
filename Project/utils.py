import os,sys
from Project.logger import logging
from Project.exception import BikeException
import pandas as pd
from Project.config import client
import yaml
import dill
from Project.config import columns_to_convert,to_convert_data


def load_data_from_db(database,collection) -> pd.DataFrame:


    try:
        logging.info(f"Reading the data from {database} and collection : {collection}")
        df =  pd.DataFrame(list(client[database][collection].find()))
        logging.info(f"The shape of data is {df.shape}")
        
        if "_id" in df.columns:
            logging.info("Droping the id column")
            df.drop("_id",axis=1,inplace=True)
        logging.info(f"The columns are: {df.columns}")
        return df
    except Exception as e:
        print(BikeException(e, error_detail = sys))


def make_report(file_path,data:dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path,"w") as fw:
            yaml.dump(data, fw)
    except Exception as e:
        print(BikeException(e, error_detail= sys))


def convert_columns(df:pd.DataFrame):
    try:
        for col in columns_to_convert:
            df[col].replace(to_convert_data[col],inplace=True)
        return df
    except Exception as e:
        print(BikeException(e, error_detail = sys))


def save_object(file_path:str,obj:object):
    try:
        logging.info("Entered the save_object method of utils")
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path,"wb") as fw:
            dill.dump(obj, fw)
        logging.info("Exited the save_object method of utils")
    except Exception as e:
        print(BikeException(e, error_detail= sys))

def r2_adj(score,x_test,y_test):
    return 1 - (1-score)*(len(y_test)-1)/(len(y_test) - x_test.shape[1]-1)


def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
         print(BikeException(e, error_detail = sys))


def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of utils")
    except Exception as e:
         print(BikeException(e, error_detail = sys))
