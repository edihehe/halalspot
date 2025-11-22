"""
models/review.py

Review model for anonymous reviews.
Reviews link to restaurants via restaurant_id (foreign key).
"""

import datetime
from utils.db import db

class Review(db.Model):
    __tablename__ = "review"

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)

    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)