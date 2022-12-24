from Project.logger import logging
from Project.exception import BikeException
import os , sys
from Project.entity import input,output
import pandas as pd
from scipy.stats  import ks_2samp
from Project import utils
from Project.entity import output
class DataValidation:
    def __init__(self,data_validation_input:input.data_validation_input, data_ingestion_output:output.data_ingestion_output):
        try:
            logging.info(f"{'--'*20} DATA VALIDATION {'--'*20}")
            self.data_validation_input = data_validation_input
            self.data_ingestion_output = data_ingestion_output
            self.validation_error = dict()
        except Exception as e:
            print(BikeException(e, error_detail = sys))


    #check do columns have null value or not (Done)
    #check there distubution against base dataframe(Done)

    def check_missing_values(self,df:pd.DataFrame) -> None:
        """This function will check if null values are there or not, as we didn't had null values in the dataset.

        Args:
            df (pd.DataFrame): data frame you want to check.

        Raises:
            BikeException: this will raise an error if null values sum is greater than zero.
        """
        try:
            null_sum =  df.isna().sum().sum()
            if null_sum != 0:
                raise BikeException("They are missing values in the dataset", error_detail = sys)
            return
        except Exception as e:
            print(BikeException(e, error_detail = sys))




    def data_drift(self,df_1:pd.DataFrame,df_2:pd.DataFrame,report_name):
        """This function check both dataset columns, that do they have same distrubtun or not and make a report out of it.

        Args:
            df_1 (pd.DataFrame): first dataframe 
            df_2 (pd.DataFrame): second dataframe
            report_name (_type_): report name 
        """
        try:
            drift_report  = dict()
            df_1_col = df_1.columns

            for col in df_1_col:
                df_1_data,df_2_data = df_1[col],df_2[col]
                same_distrubution = ks_2samp(df_1_data, df_2_data)

                if same_distrubution.pvalue > 0.05:
                    drift_report[col] = {"pvalue" : float(same_distrubution.pvalue),
                                     "same_distrubtion" : True}
                else:
                    drift_report[col] = {"pvalue" : float(same_distrubution.pvalue),
                                     "same_distrubtion" : False}

            self.validation_error[report_name] = drift_report

        except Exception as e :
            print(BikeException(e, error_detail=sys))



    def start_data_valditation(self,):
        logging.info("read the base dataframe")
        #read the base dataframe
        base_df = pd.read_csv(self.data_validation_input.base_dataframe_path)
        logging.info("read the train dataframe")
        #read the train dataframe
        train_df = pd.read_csv(self.data_ingestion_output.train_file_path)
        logging.info("read the test dataframe")
        #read the test dataframe
        test_df = pd.read_csv(self.data_ingestion_output.test_file_path)

        logging.info("Cheking for missing values in base dataframe")
        #Cheking for missing values in base dataframe 
        self.check_missing_values(base_df)
        logging.info("Cheking for missing values in train dataframe")
        #Cheking for missing values in train dataframe 
        self.check_missing_values(train_df)
        logging.info("Cheking for missing values in test dataframe")
        #Cheking for missing values in test dataframe 
        self.check_missing_values(test_df)

        logging.info("Checking data drift with base and train")
        #Checking data drift with base and train
        self.data_drift(base_df, train_df, "base and train")

        logging.info("Checking data drift with base and test")
        #Checking data drift with base and test
        self.data_drift(base_df, test_df, "base and test")

        logging.info("Checking data drift with base and test")
        #Checking data drift with test and train
        self.data_drift(test_df, train_df, "test and train")


        logging.info("Making the report")
        #Making the report
        utils.make_report(self.data_validation_input.report, self.validation_error)

        data_validation_output = output.data_validation_output(report_path = self.data_validation_input.report)
        logging.info(f"Data validation output : {data_validation_output}")
        return data_validation_output 













    

    