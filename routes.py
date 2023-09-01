# routes/user_routes.py (di dalam direktori routes)
from flask import Blueprint
from src.pipeline.recommend_pipeline import RecommendPipeline
from src.models.products import Product
from src.models.ratings import Rating
from flask import jsonify, request

recommend_bp = Blueprint('recommend_bp', __name__)
product_bp = Blueprint('product_bp', __name__)
rating_bp = Blueprint('rating_bp', __name__)


@recommend_bp.route("/recommend", methods=['POST'])
def recommend_api():
    request_data = request.get_json()
    user_id = request_data.get('user_id')
    num_neighbors = request_data.get('num_neighbors')
    num_items = request_data.get('num_items')

    recommend_pipeline=RecommendPipeline()
    results = recommend_pipeline.rating_predictor(user_id, num_neighbors, num_items)

    return jsonify(data=results)


@rating_bp.route('/ratings', methods=['GET'])
def get_ratings():
    ratings = Rating.query.limit(5).all()
    
    rating_list = []
    for rating in ratings:
        rating_data = {
            'product_id': rating.id,
            'user_id': rating.user_id,
            'product_id': rating.product_id,
            'rating': rating.rating,
        }
        rating_list.append(rating_data)
    
    return jsonify({'ratings': rating_list})


@product_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    
    product_list = []
    for product in products:
        product_data = {
            'product_id': product.product_id,
            'name': product.name,
            'merchant_id': product.merchant_id,
            'product_category_id': product.product_category_id,
            'minimal_order': product.minimal_order,
            'short_desc': product.short_desc,
            'price_value': product.price_value,
            'stock_value': product.stock_value,
            'created_at': product.created_at,
            'updated_at': product.updated_at
        }
        product_list.append(product_data)
    
    return jsonify({'products': product_list})