from dataclasses import dataclass

@dataclass
class data_ingestion_output:
    dataset_file_path :str
    train_file_path : str
    test_file_path : str


@dataclass
class data_validation_output:
    report_path : str


@dataclass
class data_tranformation_output:
    tranfomer_path : str
    transformed_train_dataset_path : str
    transformed_test_dataset_path : str
    
