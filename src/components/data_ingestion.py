import os
import pandas as pd
import sys

from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig
from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer
from src.models.ratings import Rating
from src.models.products import Product
from src.models.users import User

@dataclass
class DataIngestionConfig:
    ratings_data_path: str = os.path.join('artifacts/ingestion', 'ratings.csv')
    items_data_path: str = os.path.join('artifacts/ingestion', 'movies.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion_db(self):
        try:
            # get all rating
            ratings = Rating.query.all()
            ratings_dict = {}
            for rating in ratings:
                if 'user_id' not in ratings_dict and 'product_id' not in ratings_dict and 'rating' not in ratings_dict:
                    ratings_dict['user_id'] = [rating.user_id]
                    ratings_dict['product_id'] = [rating.product_id]
                    ratings_dict['rating'] = [rating.rating]
                else:
                    ratings_dict['user_id'].append(rating.user_id)
                    ratings_dict['product_id'].append(rating.product_id)
                    ratings_dict['rating'].append(rating.rating)

            # get all product
            products = Product.query.all()
            products_dict = {}
            products_key = ['product_id', 'name', 'merchant_id', 'product_category_id', 'minimal_order', 'short_desc', 'price_value', 'stock_value']
            for product in products:
                if all(key in products_dict for key in products_key):
                    products_dict['product_id'].append(product.product_id)
                    products_dict['name'].append(product.name)
                    products_dict['merchant_id'].append(product.merchant_id)
                    products_dict['product_category_id'].append(product.product_category_id)
                    products_dict['minimal_order'].append(product.minimal_order)
                    products_dict['short_desc'].append(product.short_desc)
                    products_dict['price_value'].append(product.price_value)
                    products_dict['stock_value'].append(product.stock_value)
                else:
                    products_dict['product_id'] = [product.product_id]
                    products_dict['name'] = [product.name]
                    products_dict['merchant_id'] = [product.merchant_id]
                    products_dict['product_category_id'] = [product.product_category_id]
                    products_dict['minimal_order'] = [product.minimal_order]
                    products_dict['short_desc'] = [product.short_desc]
                    products_dict['price_value'] = [product.price_value]
                    products_dict['stock_value'] = [product.stock_value]

            
            # get all user
            users = User.query.all()
            users_dict = {}
            users_key = ['id', 'username', 'email', 'password', 'role', 'registration_at']
            for user in users:
                if all(key in users_dict for key in users_key):
                    users_dict['id'].append(user.id)
                    users_dict['username'].append(user.username)
                    users_dict['email'].append(user.email)
                    users_dict['password'].append(user.password)
                    users_dict['role'].append(user.role)
                    users_dict['registration_at'].append(user.registration_at)
                else:
                    users_dict['id'] = [user.id]
                    users_dict['username'] = [user.username]
                    users_dict['email'] = [user.email]
                    users_dict['password'] = [user.password]
                    users_dict['role'] = [user.role]
                    users_dict['registration_at'] = [user.registration_at]


            ratings_df = pd.DataFrame(ratings_dict)
            products_df = pd.DataFrame(products_dict)
            users_df = pd.DataFrame(users_dict)
            
            return (
                ratings_df,
                products_df,
                users_df
            )
        
        except Exception as e:
            raise CustomException(e, sys)
        

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
    ratings_data, items_data = data_ingestion.initiate_data_ingestion()

    data_transformation = DataTransformation()
    transformed_ratings, transformed_items, item_user_matrix = data_transformation.initiate_data_transformation(ratings_data, items_data)

    modeltrainer=ModelTrainer()
    modeltrainer.initiate_model_trainer(item_user_matrix)



# Data Collection:
# Mengumpulkan data dari berbagai sumber seperti basis data, log penggunaan, atau layanan web. Data ini dapat berupa informasi tentang penilaian, peringkat, atau preferensi yang diberikan oleh pengguna terhadap item tertentu.

# Data Preprocessing:
# Membersihkan data mentah dari kesalahan dan duplikasi. Langkah ini dapat melibatkan deteksi dan penanganan nilai yang hilang, entri duplikat, atau outlier yang tidak wajar.

# Data Integration:
# Menggabungkan data dari berbagai sumber jika diperlukan. Misalnya, jika Anda memiliki beberapa sumber data yang berbeda, seperti penilaian dari situs web dan data pembelian dari aplikasi seluler, Anda mungkin perlu mengintegrasikan data ini menjadi satu dataset yang lebih besar.

# Data Storage:
# Menyimpan data yang telah diingest dalam format yang sesuai, seperti database atau file CSV. Penting untuk memiliki struktur data yang efisien dan mudah diakses untuk tahap selanjutnya.