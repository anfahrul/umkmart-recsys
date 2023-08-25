from flask import Flask, request, jsonify
from src.pipeline.recommend_pipeline import RecommendPipeline

app = Flask(__name__)

@app.route("/")
def hello_api():
    return {
        "app_name": "recSys App",
        "version": "v1.0.0",
        "message": "Welcome to our recommendation system engine!"
    }


@app.route("/recommend", methods=['POST'])
def recommend_api():
    request_data = request.get_json()
    user_id = request_data.get('user_id')
    num_neighbors = request_data.get('num_neighbors')
    num_items = request_data.get('num_items')

    recommend_pipeline=RecommendPipeline()
    results = recommend_pipeline.rating_predictor(user_id, num_neighbors, num_items)

    return jsonify(data=results)


if __name__=="__main__":
    app.run(host="0.0.0.0")