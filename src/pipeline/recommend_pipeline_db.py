import os
import sys
import pandas as pd

from src.exception import CustomException
from src.utils import load_object
from src.logger import logging

class RecommendPipelineDB:
    def __init__(self):
        pass


    def recommend_items(self, original_matrix, predict_matrix, user, num_items):
        try:
            recommended_items = []

            for i in original_matrix[original_matrix[user] == 0].index.tolist():
                index_df = original_matrix.index.tolist().index(i)
                predicted_rating = predict_matrix.iloc[index_df, predict_matrix.columns.tolist().index(user)]
                recommended_items.append((i, predicted_rating))

            item_sorted = sorted(recommended_items, key=lambda x:x[1], reverse=True)

            recommended_items_structured = []
            rank = 1
            for item in item_sorted[:num_items]:
                # print('{}: {} - predicted rating: {}'.format(rank, item[0], item[1]))
                recommend_item = {}
                recommend_item["predict_rank"] = rank
                recommend_item["item_id"] = item[0]
                recommend_item["predict_rating"] = int(item[1])
                recommended_items_structured.append(recommend_item)

                rank += 1

            df_rekomendasi = pd.DataFrame(recommended_items_structured)

            items_path = os.path.join("artifacts/transformation-db","items.pkl")
            items_artifact = load_object(file_path=items_path)

            recommend_items_merged = pd.merge(df_rekomendasi, items_artifact, left_on='item_id', right_on='product_id', how='inner')
            recommend_items_fix = []
            for index, row in recommend_items_merged.iterrows():
                recommend = {}
                recommend["product_id"] = row['product_id']
                recommend["name"] = row['name']
                recommend["merchant_id"] = row['merchant_id']
                recommend["product_category_id"] = row['product_category_id']
                recommend["minimal_order"] = row['minimal_order']
                recommend["short_desc"] = row['short_desc']
                recommend["price_value"] = row['price_value']
                recommend["stock_value"] = row['stock_value']
                recommend["predict_rank"] = row['predict_rank']
                recommend["predict_rating"] = row['predict_rating']
                recommend_items_fix.append(recommend)

            
            logging.info("Item has recommended successfully")
            return recommend_items_fix            
        
        except Exception as e:
            raise CustomException(e,sys)
    

    def rating_predictor(self, user, num_neighbors, num_recommendation):
        try:
            model_path=os.path.join("artifacts/model-db","knn_model.pkl")
            model=load_object(file_path=model_path)
            item_user_matrix_path=os.path.join("artifacts/transformation-db","item_user_matrix.pkl")
            item_user_matrix=load_object(file_path=item_user_matrix_path)
            logging.info("Load model and item user matrix completed")


            model.fit(item_user_matrix.values)
            distances, indices = model.kneighbors(item_user_matrix.values, n_neighbors=num_neighbors)
            predict_matrix = item_user_matrix.copy()

            user_index = item_user_matrix.columns.tolist().index(user)

            for idx_item, t in list(enumerate(item_user_matrix.index)):
                if item_user_matrix.iloc[idx_item, user_index] == 0:
                    sim_items = indices[idx_item].tolist()
                    item_distances = distances[idx_item].tolist()

                    if idx_item in sim_items:
                        id_item = sim_items.index(idx_item)
                        sim_items.remove(idx_item)
                        item_distances.pop(id_item)
                    else:
                        sim_items = sim_items[:num_neighbors-1]
                        item_distances = item_distances[:num_neighbors-1]
                    
                    item_similarity = [1-x for x in item_distances]
                    item_similarity_copy = item_similarity.copy()
                    nominator = 0

                    for idx_of_similarity in range (0, len(item_similarity)):
                        if item_user_matrix.iloc[sim_items[idx_of_similarity], user_index] == 0:
                            if len(item_similarity_copy) == (num_neighbors-1):
                                item_similarity_copy.pop(idx_of_similarity)
                            else:
                                item_similarity_copy.pop(idx_of_similarity-(len(item_similarity)-len(item_similarity_copy)))
                        
                        else:
                            nominator += item_similarity[idx_of_similarity] * item_user_matrix.iloc[sim_items[idx_of_similarity], user_index]
                    
                    if len(item_similarity) > 0:
                        if sum(item_similarity_copy) > 0:
                            predicted_r = nominator / sum(item_similarity_copy)
                        else:
                            predicted_r = 0
                    
                    else:
                        predicted_r = 0

                    predict_matrix.iloc[idx_item, user_index] = predicted_r
            logging.info("Predict rating calculation completed")

            return self.recommend_items(item_user_matrix, predict_matrix, user, num_recommendation)
        
        except Exception as e:
            raise CustomException(e,sys)   