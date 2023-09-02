import os
import sys
from dataclasses import dataclass

import pandas as pd
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationDBConfig:
    itemusermatrix_obj_file_path = os.path.join('artifacts/transformation-db', 'item_user_matrix.pkl')
    items_obj_file_path = os.path.join('artifacts/transformation-db', 'items.pkl')
    users_obj_file_path = os.path.join('artifacts/transformation-db', 'users.pkl')

class DataTransformationDB:
    def __init__(self):
        self.data_transformation_config = DataTransformationDBConfig()


    def filter_popularity(self, ratings_df, popularity_threshold):
        try:
            df_product_count = pd.DataFrame(ratings_df.groupby('product_id').size(), columns=['count'])
            popular_product = list(set(df_product_count.query(f'count >= {popularity_threshold}').index))
            filtered_items_rating_df = ratings_df[ratings_df.product_id.isin(popular_product)]
            
            print('Shape of original rating data:', ratings_df.shape)
            print('Shape of rating data after dropping unpopular movie:', filtered_items_rating_df.shape)
            
            logging.info("Filtered popularity items completed")
            return filtered_items_rating_df
        
        except Exception as e:
            raise CustomException(e, sys)
    

    def drop_unpopular_users(self, original_ratings_df,  ratings_df, popularity_threshold):
        try:
            df_user_count = pd.DataFrame(ratings_df.groupby('user_id').size(), columns=['count'])
            popular_user = list(set(df_user_count.query(f'count >= {popularity_threshold}').index))
            filtered_users_rating_df = ratings_df[ratings_df.user_id.isin(popular_user)]
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
            item_user_matrix = transformed_ratings.pivot_table(index='product_id', columns='user_id', values='rating', fill_value=0)

            logging.info("Creating item user matrix completed")
            return item_user_matrix
        
        except Exception as e:
            raise CustomException(e, sys)


    def initiate_data_transformation(self, ratings_df, items_df, users_df):
        try:
            filtered_items_rating_df = self.filter_popularity(ratings_df, 50)
            filtered_users_rating_df = self.drop_unpopular_users(ratings_df, filtered_items_rating_df, 3)
            # is_coloumns_used_ratings_df = self.drop_unused_columns(filtered_users_rating_df)
            # transformed_ratings, transformed_items = self.rename_columns(is_coloumns_used_ratings_df, items_df)
            
            # item_user_matrix = self.pivot_to_matrix(filtered_users_rating_df)
            item_user_matrix = self.pivot_to_matrix(ratings_df)
            logging.info("Transformer process completed")

            save_object(
                file_path=self.data_transformation_config.itemusermatrix_obj_file_path,
                obj=item_user_matrix
            )
            save_object(
                file_path=self.data_transformation_config.items_obj_file_path,
                obj=items_df
            )
            save_object(
                file_path=self.data_transformation_config.users_obj_file_path,
                obj=users_df
            )
            logging.info("Saving object completed")

            return (
                self.data_transformation_config.itemusermatrix_obj_file_path,
                self.data_transformation_config.items_obj_file_path,
                self.data_transformation_config.users_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)