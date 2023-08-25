import os
import sys
from dataclasses import dataclass

from sklearn.neighbors import NearestNeighbors

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object, load_object

@dataclass
class ModelTrainerConfig:
    model_file_path=os.path.join("artifacts/model","knn_model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()


    def initiate_model_trainer(self, item_user_matrix_path):
        try:
            # item_user_matrix_path=os.path.join("artifacts","model.pkl")
            item_user_matrix=load_object(file_path=item_user_matrix_path)
            model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10, n_jobs=-1)
            model.fit(item_user_matrix.values)
            logging.info("KNN Modeling completed")

            save_object(
                file_path=self.model_trainer_config.model_file_path,
                obj=model
            )
            logging.info("Saving model completed")

        except Exception as e:
            raise CustomException(e,sys)