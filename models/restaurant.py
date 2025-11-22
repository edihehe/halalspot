"""
models/restaurant.py

Restaurant model maps to a restaurants table in the database.
Each instance is one restaurant row.
"""

from utils.db import db

class Restaurant(db.Model):
    __tablename__ = "restaurant"

    id = db.Column(db.Integer, primary_key=True)

    # Basic fields
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(255))

    # Coordinates, used by the map
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    # Additional metadata
    cuisine = db.Column(db.String(100))
    halal_status = db.Column(db.String(100))
    image_url = db.Column(db.String(255))

    # NOTE: we do not define a relationship here explicitly (simple approach)
    # If you want: reviews = db.relationship('Review', backref='restaurant', lazy=True)
    # But for simplicity we will query reviews by restaurant_id in routes.