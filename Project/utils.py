import os,sys
from Project.logger import logging
from Project.exception import BikeException
import pandas as pd
from Project.config import client

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

