import os,sys
from Project.logger import logging
from Project.exception import BikeException
from Project.entity import input,output
from sklearn.linear_model import Ridge
import pandas as pd
from Project.config import TARGET_COLUMN
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
from Project import utils
class ModelTraining:
    def __init__(self,model_training_input:input.model_training_input,
                      data_tranformation_output:output.data_tranformation_output):
        try:
            logging.info(f"{'--'*20} MODEL TRAINING {'--'*20}")
            self.model_training_input = model_training_input
            self.data_tranformation_output = data_tranformation_output
            self.accuracy_report = dict()
        except Exception as e:
            print(BikeException(e, error_detail = sys))


    #Read train data and test data
    #fit the Model
    #save the model file
    #save the accuracy 

    def start_model_training(self,):
        try:
            logging.info("Reading both train and test file")
            #Reading train file
            train = pd.read_csv(self.data_tranformation_output.transformed_train_dataset_path)
            #Reading test file 
            test = pd.read_csv(self.data_tranformation_output.transformed_test_dataset_path)

            logging.info("Spliting them into X_train,x_test and Y_train,y_test")
            logging.info("making X_train and x_test")
            #making X_train and x_test
            X_train = train.drop(TARGET_COLUMN,axis=1)
            x_test = test.drop(TARGET_COLUMN,axis=1)
            logging.info(f"{(X_train.shape,x_test.shape)}")
           
            logging.info("making Y_train and y_test")
            #making Y_train and y_test
            Y_train = train[TARGET_COLUMN]
            y_test = test[TARGET_COLUMN]
            logging.info(f"{(Y_train.shape,y_test.shape)}")
            logging.info("Making the model")
            model = Ridge()
            #fiting the model 
            logging.info("fitting the model with X_train and Y_train")
            model.fit(X_train, Y_train)
            logging.info("Done fiting")

            logging.info("making prediction")
            #making prediction
            y_pred = model.predict(x_test)

            logging.info("Getting the accuracy score")
            #getting the accuracy score
            training_score = model.score(X_train, Y_train)
            r2 = r2_score(y_test, y_pred)
            r2_adjested = utils.r2_adj(r2, x_test, y_test)
            MAE = mean_absolute_error(y_test, y_pred)
            MSE = mean_squared_error(y_test, y_pred)
            

            logging.info(f" training_score : {training_score}, r2 : {r2}, r2_adjested : {r2_adjested}, MAE : {MAE}, MSE : {MSE}")

            self.accuracy_report["model"] = "Ridge"
            self.accuracy_report["training_score"] = float(training_score)
            self.accuracy_report["r2-score"] = float(r2)
            self.accuracy_report["r2_adjested"] = float(r2_adjested)
            self.accuracy_report["MAE"]  = float(MAE)
            self.accuracy_report["MSE"] = float(MSE)

            logging.info("saving the model file")
            #saving the model file 
            utils.save_object(file_path = self.model_training_input.model_file_path, obj = model)

            logging.info("saving the accuracy report")
            utils.make_report(file_path = self.model_training_input.accuracy_report_path, data = self.accuracy_report)

            logging.info("making the output")
            #making the output

            model_training_output = output.model_training_output(model_file_path = self.model_training_input.model_file_path, 
                                                                accuracy_report_path = self.model_training_input.accuracy_report_path)
            return model_training_output

        except Exception as e:
            print(BikeException(e, error_detail = sys))