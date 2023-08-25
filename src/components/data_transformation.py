import os
import sys
from dataclasses import dataclass

import pandas as pd
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    itemusermatrix_obj_file_path = os.path.join('artifacts/transformation', 'item_user_matrix.pkl')
    items_obj_file_path = os.path.join('artifacts/transformation', 'items.pkl')
    ratings_obj_file_path = os.path.join('artifacts/transformation', 'ratings.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()


    def filter_popularity(self, ratings_df, popularity_threshold=50):
        try:
            dfMoviesCount = pd.DataFrame(ratings_df.groupby('movieId').size(), columns=['count'])
            popularMovie = list(set(dfMoviesCount.query(f'count >= {popularity_threshold}').index))
            filtered_items_rating_df = ratings_df[ratings_df.movieId.isin(popularMovie)]
            
            print('Shape of original rating data:', ratings_df.shape)
            print('Shape of rating data after dropping unpopular movie:', filtered_items_rating_df.shape)
            
            logging.info("Filtered popularity items completed")
            return filtered_items_rating_df
        except Exception as e:
            raise CustomException(e, sys)
    

    def drop_unpopular_users(self, original_ratings_df,  ratings_df, popularity_threshold=50):
        try:
            dfUserCount = pd.DataFrame(ratings_df.groupby('userId').size(), columns=['count'])
            popularUser = list(set(dfUserCount.query(f'count >= {popularity_threshold}').index))
            filtered_users_rating_df = ratings_df[ratings_df.userId.isin(popularUser)]
            filtered_users_rating_df.reset_index(drop=True, inplace=True)
            
            print('Shape of original rating data:', original_ratings_df.shape)
            print('Shape of rating data after dropping unpopular user:', filtered_users_rating_df.shape)
            logging.info("Filtered popularity users completed")
            return filtered_users_rating_df
        except Exception as e:
            raise CustomException(e, sys)
    
    
    def drop_unused_columns(self, ratings_df):
        try:
            is_used_ratings_df = ratings_df.drop(columns=['timestamp'])

            logging.info("Drop unwanted column completed")
            return is_used_ratings_df
        except Exception as e:
            raise CustomException(e, sys)
    
    
    def rename_columns(self, ratings_df, items_df):
        try:
            renaming_ratings_df = ratings_df.rename(columns={
                "userId": "user_id",
                "movieId": "movie_id"
            })
            
            renaming_items_df = items_df.rename(columns={
                "movieId": "movie_id"
            })
            
            logging.info("renaming column ratings and items completed")
            return renaming_ratings_df, renaming_items_df
        except Exception as e:
            raise CustomException(e, sys)
    
    
    def pivot_to_matrix(self, transformed_ratings):
        try:
            item_user_matrix = transformed_ratings.pivot_table(index='movie_id', columns='user_id', values='rating', fill_value=0)
            item_user_matrix.reset_index(drop=True, inplace=True)
            item_user_matrix.columns = range(len(item_user_matrix.columns))
            
            logging.info("Creating item user matrix completed")
            return item_user_matrix
        except Exception as e:
            raise CustomException(e, sys)


    def initiate_data_transformation(self, ratings_data, items_data):
        try:
            ratings_df = pd.read_csv(ratings_data)
            items_df = pd.read_csv(items_data)
            logging.info("Read ratings_df and items_df completed")

            filtered_items_rating_df = self.filter_popularity(ratings_df, 50)
            filtered_users_rating_df = self.drop_unpopular_users(ratings_df, filtered_items_rating_df, 50)
            is_coloumns_used_ratings_df = self.drop_unused_columns(filtered_users_rating_df)
            transformed_ratings, transformed_items = self.rename_columns(is_coloumns_used_ratings_df, items_df)
            
            item_user_matrix = self.pivot_to_matrix(transformed_ratings)
            logging.info("Transformer process completed")

            save_object(
                file_path=self.data_transformation_config.itemusermatrix_obj_file_path,
                obj=item_user_matrix
            )
            save_object(
                file_path=self.data_transformation_config.items_obj_file_path,
                obj=transformed_items
            )
            save_object(
                file_path=self.data_transformation_config.ratings_obj_file_path,
                obj=transformed_ratings
            )
            logging.info("Saving object completed")

            return (
                self.data_transformation_config.itemusermatrix_obj_file_path,
                self.data_transformation_config.items_obj_file_path,
                self.data_transformation_config.ratings_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)


# Data Cleaning:
# Identifikasi dan penanganan data yang hilang, duplikat, atau tidak valid. Misalnya, jika terdapat penilaian yang hilang, Anda perlu memutuskan apakah akan mengisi nilai yang hilang atau memperlakukan data tersebut secara berbeda.

# Data Normalization:
# Mengubah data ke dalam skala yang seragam. Ini penting untuk mencegah perbedaan skala yang dapat mempengaruhi kualitas rekomendasi. Misalnya, mengubah peringkat pengguna ke dalam skala antara 0 dan 1.

# User-Item Matrix Creation:
# Membentuk matriks pengguna-item, di mana setiap baris mewakili pengguna dan setiap kolom mewakili item. Entri matriks dapat berisi informasi seperti peringkat atau interaksi pengguna dengan item. Matriks ini merupakan dasar untuk algoritma collaborative filtering.

# Feature Engineering:
# Menciptakan fitur tambahan yang dapat meningkatkan kualitas rekomendasi. Ini bisa berupa informasi tentang pengguna (misalnya, lokasi, usia) atau informasi tentang item (misalnya, genre film). Fitur-fitur ini dapat membantu model rekomendasi memahami preferensi pengguna dengan lebih baik.

# Handling Sparse Data:
# Jika terdapat banyak entri yang hilang dalam matriks pengguna-item, diperlukan strategi untuk mengatasi masalah data yang tidak lengkap. Teknik seperti imputasi (mengisi nilai yang hilang dengan nilai perkiraan) dapat digunakan.