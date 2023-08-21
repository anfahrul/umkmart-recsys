import os
import pandas as pd
import sys
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging

@dataclass
class DataIngestionConfig:
    ratings_data_path: str = os.path.join('artifacts/ingestion', 'ratings.csv')
    items_data_path: str = os.path.join('artifacts/ingestion', 'movies.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")

        try:
            df_ratings = pd.read_csv('data/movies_dataset/ratings.csv')
            df_items = pd.read_csv('data/movies_dataset/movies.csv')
            logging.info('Read the dataset as dataframe')
            
            os.makedirs(os.path.dirname(self.ingestion_config.items_data_path), exist_ok=True)
            
            df_ratings.to_csv(self.ingestion_config.ratings_data_path, index=False, header=True)
            df_items.to_csv(self.ingestion_config.items_data_path, index=False, header=True)
            
            logging.info("Inmgestion of the data iss completed")
            return(
                self.ingestion_config.ratings_data_path,
                self.ingestion_config.items_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    data_ingestion = DataIngestion()
    train_data, test_data = data_ingestion.initiate_data_ingestion()

    # Continue with the next steps, such as data transformation and model training



# Data Collection:
# Mengumpulkan data dari berbagai sumber seperti basis data, log penggunaan, atau layanan web. Data ini dapat berupa informasi tentang penilaian, peringkat, atau preferensi yang diberikan oleh pengguna terhadap item tertentu.

# Data Preprocessing:
# Membersihkan data mentah dari kesalahan dan duplikasi. Langkah ini dapat melibatkan deteksi dan penanganan nilai yang hilang, entri duplikat, atau outlier yang tidak wajar.

# Data Integration:
# Menggabungkan data dari berbagai sumber jika diperlukan. Misalnya, jika Anda memiliki beberapa sumber data yang berbeda, seperti penilaian dari situs web dan data pembelian dari aplikasi seluler, Anda mungkin perlu mengintegrasikan data ini menjadi satu dataset yang lebih besar.

# Data Storage:
# Menyimpan data yang telah diingest dalam format yang sesuai, seperti database atau file CSV. Penting untuk memiliki struktur data yang efisien dan mudah diakses untuk tahap selanjutnya.