from dataclasses import dataclass

@dataclass
class data_ingestion_output:
    dataset_file_path :str
    train_file_path : str
    test_file_path : str

    