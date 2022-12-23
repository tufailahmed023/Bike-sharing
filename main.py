from Project.entity.input import training_pipeline_input,data_ingestion_input
from Project.components.data_ingestion import DataIngestion

train = training_pipeline_input()
data = data_ingestion_input(train)
obj = DataIngestion(data)
data_ingestion_output = obj.start_data_ingestion()


