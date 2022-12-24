import os , sys
from Project.logger import logging
from Project.exception import BikeException
from Project.entity import input,output
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.pipeline import Pipeline
import pandas as pd
from Project import utils,config
from Project.config import columns_to_convert,columns_to_drop

class DataTransformation:
    def __init__(self,data_tranformation_input:input.data_tranformation_input,
                     data_ingestion_output:output.data_ingestion_output):

        try:
            logging.info(f"{'--'*20} DATA TRANSFORMATION {'--'*20}")
            self.data_tranformation_input = data_tranformation_input
            self.data_ingestion_output = data_ingestion_output
        except Exception as e:
            print(BikeException(e, error_detail = sys))


    @classmethod
    def data_transformer(cls):
        try:
            scaler = StandardScaler()
            pipeline = Pipeline(steps = [("StandardScaler",scaler)])
            return pipeline
        except Exception as e:
            print(BikeException(error_message = e, error_detail = sys))


    def start_data_tranformation(self,):
        try:
            logging.info("Reading both files")
            #reading train file
            train_df = pd.read_csv(self.data_ingestion_output.train_file_path) 
            #reading test file
            test_df = pd.read_csv(self.data_ingestion_output.test_file_path)
            logging.info(f"{(train_df.shape,test_df.shape)}")
            logging.info("Converting columns to catorigal")
            #convert columns to catorigal
            train_converted = utils.convert_columns(train_df)
            test_converted = utils.convert_columns(test_df)

            logging.info("One hot encoding Train data")
            #onehot encoding
            #train data
            train_converted = pd.get_dummies(data = train_converted, columns=columns_to_convert[:-1],drop_first=True)
            train_converted = pd.get_dummies(data = train_converted, columns=[columns_to_convert[-1]],drop_first=True)

            logging.info("One hot encoding Test data")
            #test data
            test_converted = pd.get_dummies(data = test_converted, columns=columns_to_convert[:-1],drop_first=True)
            test_converted = pd.get_dummies(data = test_converted, columns=[columns_to_convert[-1]],drop_first=True)

            logging.info("Scaling the data")
            #Scaling the data
            #getting the tranformation Pipeline
            transformation_pipeline = DataTransformation.data_transformer()
            transformation_pipeline.fit(train_converted[config.countinous_columns])

            logging.info("Fited the train data to trasformation pipline")
            #Transforming the data
            logging.info("Tranforming both data's continous columns")
            train_converted[config.countinous_columns] = transformation_pipeline.transform(train_converted[config.countinous_columns])
            test_converted[config.countinous_columns] = transformation_pipeline.transform(test_converted[config.countinous_columns])
            logging.info("Tranforming done on both data's continous columns")

            logging.info(f"Droping not needed columns : {columns_to_drop}")
            train_converted.drop(columns_to_drop,axis=1,inplace=True)
            test_converted.drop(columns_to_drop,axis=1,inplace=True)

            logging.info("Saving the tranformation object")
            #Saving the tranformation object
            utils.save_object(self.data_tranformation_input.tranformer_path, transformation_pipeline)

            logging.info("Saving train_converted")
            #Saving train_converted
            con_train_dir = os.path.dirname(self.data_tranformation_input.tranfomed_train_data)
            os.makedirs(con_train_dir,exist_ok=True)
            train_converted.to_csv(self.data_tranformation_input.tranfomed_train_data,index=False,header=True)

            logging.info("Saving test_converted")
            #Saving test_converted
            con_test_dir = os.path.dirname(self.data_tranformation_input.tranfomed_test_data)
            os.makedirs(con_test_dir,exist_ok=True)
            test_converted.to_csv(self.data_tranformation_input.tranfomed_test_data,index=False,header=True)


            logging.info("making the output")
            #making the output 
            data_tranformation_output = output.data_tranformation_output(tranfomer_path = self.data_tranformation_input.tranformer_path, 
                                                                         transformed_train_dataset_path = self.data_tranformation_input.tranfomed_train_data, 
                                                                         transformed_test_dataset_path = self.data_tranformation_input.tranfomed_test_data)
            logging.info(f"Data tranformation output : {data_tranformation_output}")

            return data_tranformation_output

        except Exception as e:
            print(BikeException(e, error_detail = sys))
