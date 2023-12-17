# models.py

from flask_login import UserMixin
from datetime import datetime
from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    predictions = db.relationship('Prediction', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_company = db.Column(db.String(50), nullable=False)
    car_model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    showroom = db.Column(db.String(100), nullable=False)
    engine_type = db.Column(db.String(10), nullable=False)
    kms = db.Column(db.Integer, nullable=False)
    date_predicted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Prediction('{self.car_company}', '{self.car_model}', '{self.date_predicted}')"
