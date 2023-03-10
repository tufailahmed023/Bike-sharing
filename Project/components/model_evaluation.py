import os, sys
from Project.logger import logging
from Project.exception import BikeException
from Project.entity import input,output
from Project.predictor import ModelResolver
from Project import utils
import pandas as pd
from Project.config import TARGET_COLUMN
from sklearn.metrics import r2_score
from Project.config import columns_to_convert,columns_to_drop
class ModelEvaluation:
    def __init__(self, 
                    model_evaluatiion_input:input.model_evaluatiion_input,
                    model_training_output:output.model_training_output,
                    data_tranformation_output:output.data_tranformation_output,
                    data_ingestion_output:output.data_ingestion_output):
        try:
            logging.info(f"{'--'*20} MODEL EVALUATION {'--'*20}")
            self.model_evaluatiion_input = model_evaluatiion_input
            self.model_training_output = model_training_output
            self.data_tranformation_output = data_tranformation_output
            self.data_ingestion_output = data_ingestion_output
            self.model_resolver = ModelResolver()
        except Exception as e:
            print(BikeException(e, error_detail = sys))

    def start_model_evualtion(self,):
        try:
            logging.info("Checking if any folder exist or not in saved model folder")
            latest_dir_path = self.model_resolver.latest_dir_path()
            if not latest_dir_path:
                logging.info("No model exist it")
                model_evaluatiion_output = output.model_evaluatiion_output(is_model_accepted = True, improved_accuracy = None)
                logging.info(f'model_evaluatiion_output : {model_evaluatiion_output}')
                return model_evaluatiion_output

            logging.info("there exist a dir in saved model folder")
            logging.info("getting the model path")
            saved_model_model_path = self.model_resolver.latest_model_path()
            logging.info("getting the transformer path")
            saved_model_transformer_path = self.model_resolver.latest_transformer_path()

            #loading saved model and transformer
            logging.info("loading the model from saved model folder")
            model_sm = utils.load_object(file_path = saved_model_model_path)
            logging.info("laoding the tranformer from saved model folder") 
            transformer_sm = utils.load_object(file_path = saved_model_transformer_path)
            ############################################################################

            #loading current model and transformer
            logging.info("loading the current model")
            model_cr = utils.load_object(file_path = self.model_training_output.model_file_path)
            logging.info("loading the current transformer")
            transformer_cr = utils.load_object(file_path = self.data_tranformation_output.tranfomer_path)
            #####################################################################################

            #loading test data
            logging.info("loading the test data and doing all the conversion")
            test_df = pd.read_csv(self.data_ingestion_output.test_file_path)
            logging.info(f"Columns are : {test_df.columns}")
            traget_df = test_df[TARGET_COLUMN]
            test_df.drop(TARGET_COLUMN,axis=1,inplace=True)
            logging.info(f"Columns after droping are : {test_df.columns}")
            logging.info(f"{traget_df.shape}")

            logging.info("doing the droping and converting")
            test_df.drop(columns_to_drop,axis = 1,inplace=True)
            #droping done
            logging.info("droping done")
            
            #converting col to cat variable
            logging.info("converting columns to catorigal variable")
            test_df = utils.convert_columns(test_df)
            logging.info("getting the dummies")
            test_df = pd.get_dummies(data = test_df, columns=columns_to_convert[:-1],drop_first=False)
            test_df = pd.get_dummies(data = test_df, columns=[columns_to_convert[-1]],drop_first=False)
            logging.info("droping and converting are done")
            #########################################################################################

            logging.info("Starting the evaluation between both models")
            ###########################################################################
            logging.info("geting accuracy score from current model")
            transformed_features = list(transformer_cr.feature_names_in_)
            test_cr = test_df
            logging.info(f"Columns are : {test_cr.columns}")
            test_cr[transformed_features] = transformer_cr.transform(test_cr[transformed_features])
            logging.info(f"Columns after tarnsform are : {test_cr.columns}")
            y_pred_cr = model_cr.predict(test_cr)
            current_model_score = float((r2_score(traget_df, y_pred_cr)))
            logging.info(f"Current model R2 score is  : {current_model_score}")
            ###########################################################################


           #loading test data
            logging.info("DOING THE SAME DATA CONVERSION AGAIN")
            logging.info("loading the test data and doing all the conversion")
            test_df = pd.read_csv(self.data_ingestion_output.test_file_path)
            logging.info(f"Columns are : {test_df.columns}")
            traget_df = test_df[TARGET_COLUMN]
            test_df.drop(TARGET_COLUMN,axis=1,inplace=True)
            logging.info(f"Columns after droping are : {test_df.columns}")
            logging.info(f"{traget_df.shape}")

            logging.info("doing the droping and converting")
            test_df.drop(columns_to_drop,axis = 1,inplace=True)
            #droping done
            logging.info("droping done")
            
            #converting col to cat variable
            logging.info("converting columns to catorigal variable")
            test_df = utils.convert_columns(test_df)
            logging.info("getting the dummies")
            test_df = pd.get_dummies(data = test_df, columns=columns_to_convert[:-1],drop_first=False)
            test_df = pd.get_dummies(data = test_df, columns=[columns_to_convert[-1]],drop_first=False)
            logging.info("droping and converting are done")

            ##################################################################################
            logging.info("getting accuracy score from saved model folder model/previous model")
            transformed_features = list(transformer_sm.feature_names_in_)
            test_sm = test_df
            test_sm[transformed_features] = transformer_sm.transform(test_sm[transformed_features])
            y_pred_sm = model_sm.predict(test_sm)
            previous_model_score = float((r2_score(traget_df, y_pred_sm)))
            logging.info(f"Previous model R2 score is  : {previous_model_score}")
            ####################################################################################
            
            logging.info("Comparing both model accuracy score")
            if current_model_score < previous_model_score:
                logging.info("Current model is not better than previous model")
                raise Exception("Current model is not better than previous model")
            
            logging.info("Current trained model is greater or equal in accuracy")
            model_evaluatiion_output = output.model_evaluatiion_output(is_model_accepted = True, improved_accuracy = float((current_model_score - previous_model_score)))
            logging.info(f"model evaluation output : {model_evaluatiion_output}")
            return model_evaluatiion_output
        except Exception as e:
            print(BikeException(e, error_detail = sys))

