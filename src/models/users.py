# src/models/product.py
from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    email_verified_at = db.Column(db.TIMESTAMP)
    password = db.Column(db.String(255))
    role = db.Column(db.Enum('user', 'system-admin'))
    remember_token = db.Column(db.String(100))
    registration_at = db.Column(db.Integer)