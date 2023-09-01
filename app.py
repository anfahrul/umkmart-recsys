from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/recsys'
db = SQLAlchemy(app)

@app.route("/")
def hello_api():
    return {
        "app_name": "recSys App",
        "version": "v1.0.0",
        "message": "Welcome to our recommendation engine!"
    }

from routes import product_bp, recommend_bp, rating_bp
app.register_blueprint(product_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(rating_bp)


if __name__=="__main__":
    app.run(host="0.0.0.0")