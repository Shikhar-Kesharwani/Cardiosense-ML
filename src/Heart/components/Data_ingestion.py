import os
import sys
import numpy as np
import pandas as pd
from src.Heart.logger import logging
from src.Heart.exception import customexception
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from pathlib import Path

class DataIngestionConfig:
    def __init__(self, dataset_type):
        self.raw_data_path:str = os.path.join("models", f"raw_data_{dataset_type}.csv")
        self.train_data_path:str = os.path.join("models", f"train_data_{dataset_type}.csv")
        self.test_data_path:str = os.path.join("models", f"test_data_{dataset_type}.csv")
        self.dataset_type = dataset_type

class DataIngestion:
    def __init__(self, dataset_type):
        self.ingestion_config = DataIngestionConfig(dataset_type)

    def initiate_data_ingestion(self):
        logging.info(f"Data ingestion started for {self.ingestion_config.dataset_type}")
        try:
            source_file = f"Notebook_Experiments/Data/heart_{self.ingestion_config.dataset_type}.csv"
            data = pd.read_csv(source_file)
            data.replace('?', np.nan, inplace=True)
            # Ensure target is float
            if 'target' in data.columns:
                data['target'] = pd.to_numeric(data['target'], errors='coerce')
                # UCI target is 0-4, we just want 0 or 1 (heart disease presence)
                if self.ingestion_config.dataset_type == 'uci':
                    data['target'] = data['target'].apply(lambda x: 1.0 if float(x) > 0 else 0.0)
            logging.info("Read the Data from the csv file and cleaned missing values")

            os.makedirs(os.path.dirname(os.path.join(self.ingestion_config.raw_data_path)), exist_ok=True)
            data.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info("Created the raw data file")

            logging.info("Splitting the data into train and test")
            train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
            logging.info("Data Splitting is done")

            train_data.to_csv(self.ingestion_config.train_data_path, index=False)
            test_data.to_csv(self.ingestion_config.test_data_path, index=False)
            logging.info("Created the train and test data files")
            logging.info("Data ingestion completed")

            # NOTE: test is returned before train in original code for some reason, keeping it to avoid breaking Training_pipeline
            return (
                self.ingestion_config.test_data_path,
                self.ingestion_config.train_data_path
            )
        except Exception as e:
            logging.info("Exception occured while ingesting the data")
            raise customexception(e,sys)