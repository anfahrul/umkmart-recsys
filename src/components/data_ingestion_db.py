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


class DataIngestionDB:
    def __init__(self):
        pass

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