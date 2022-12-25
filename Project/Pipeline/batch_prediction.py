import os,sys
from Project.exception import BikeException
from Project.logger import logging
from Project.predictor import ModelResolver
import pandas as pd
from Project import utils
from Project.config import columns_to_drop,columns_to_convert
from datetime import datetime

PRIDICTION_DIR = 'prediction'

def strart_batch_prediction(input_file_path):
    try:
        logging.info(f"{'--'*20} BATCH PREDICTION {'--'*20}")
        os.makedirs(PRIDICTION_DIR,exist_ok=True)
        logging.info("creating model resolver object")
        model_resolver = ModelResolver()  
        logging.info(f"Reading file from path {input_file_path}")
        df = pd.read_csv(f"{input_file_path}")
        
        logging.info("droping unwanted columns")
        df.drop(columns_to_drop,axis = 1, inplace = True)

        logging.info("converting columns")
        df = utils.convert_columns(df)
        df = pd.get_dummies(data = df, columns=columns_to_convert[:-1],drop_first=True)
        df = pd.get_dummies(data = df, columns=[columns_to_convert[-1]],drop_first=True)

        logging.info("getting the transformer")
        transformer = utils.load_object(model_resolver.latest_transformer_path())
        logging.info("tansforming the data")
        
        featurs = list(transformer.feature_names_in_)

        df[featurs] = transformer.transform(df[featurs])

        logging.info("geting the model")
        model = utils.load_object(model_resolver.latest_model_path())

        logging.info("making prediction")
        prediction = model.predict(df)
        df["prediction"] = prediction

        prediction_file_name = os.path.basename(input_file_path).replace(".csv",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        prediction_file_path = os.path.join(PRIDICTION_DIR,prediction_file_name)
        df.to_csv(prediction_file_path,index=False,header=True)
        logging.info(f"Prediction file in : {prediction_file_path}")
        return prediction_file_path
    except Exception as e:
        print(BikeException(e, error_detail = sys))