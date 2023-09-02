import os
import sys
from dataclasses import dataclass

from sklearn.neighbors import NearestNeighbors

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object, load_object

@dataclass
class ModelTrainerConfigDB:
    model_file_path=os.path.join("artifacts/model-db","knn_model.pkl")

class ModelTrainerDB:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfigDB()


    def initiate_model_trainer(self, item_user_matrix_path, num_neighbors):
        try:
            item_user_matrix=load_object(file_path=item_user_matrix_path)
            model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=num_neighbors, n_jobs=-1)
            model.fit(item_user_matrix.values)
            logging.info("KNN Modeling completed")

            save_object(
                file_path=self.model_trainer_config.model_file_path,
                obj=model
            )

            return self.model_trainer_config.model_file_path
            logging.info("Saving model completed")

        except Exception as e:
            raise CustomException(e,sys)