# src/models/rating.py
from app import db

class Rating(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36))
    product_id = db.Column(db.String(36))
    rating = db.Column(db.Integer)