# src/models/product.py
from app import db

class Product(db.Model):
    __tablename__ = 'products'
    
    product_id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(255))
    merchant_id = db.Column(db.String(36))
    product_category_id = db.Column(db.BigInteger)
    minimal_order = db.Column(db.Integer)
    short_desc = db.Column(db.Text)
    price_value = db.Column(db.Integer)
    stock_value = db.Column(db.Integer)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)