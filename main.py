from Project.entity.input import training_pipeline_input,data_ingestion_input,data_validation_input,data_tranformation_input,model_training_input
from Project.components.data_ingestion import DataIngestion
from Project.components.data_validation import DataValidation
from Project.components.data_transformation import DataTransformation
from Project.components.model_training import ModelTraining

train = training_pipeline_input()
data = data_ingestion_input(train)
obj = DataIngestion(data)
data_ingestion_output = obj.start_data_ingestion()


data1 = data_validation_input(train)
obj1 = DataValidation(data1, data_ingestion_output)
data_validation_output = obj1.start_data_valditation()


data2 = data_tranformation_input(train)
obj2 = DataTransformation(data2, data_ingestion_output)
data_tranformation_output = obj2.start_data_tranformation()


data3 = model_training_input(train)
obj3 = ModelTraining(data3, data_tranformation_output)
model_training_output = obj3.start_model_training()