from Project.entity.input import training_pipeline_input,data_ingestion_input,data_validation_input
from Project.components.data_ingestion import DataIngestion
from Project.components.data_validation import DataValidation

train = training_pipeline_input()
data = data_ingestion_input(train)
obj = DataIngestion(data)
data_ingestion_output = obj.start_data_ingestion()


data1 = data_validation_input(train)
obj1 = DataValidation(data1, data_ingestion_output)
data_validation_output = obj1.start_data_valditation()