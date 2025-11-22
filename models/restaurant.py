"""
models/restaurant.py

Restaurant model maps to the restaurant table in the database.
"""

from utils.db import db  # Make sure this points to your SQLAlchemy instance

class Restaurant(db.Model):
    __tablename__ = "restaurant"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    cuisine = db.Column(db.String(100))
    halal_status = db.Column(db.String(100))
    image_url = db.Column(db.String(255))

    # Convert object to dictionary for JSON serialization
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "cuisine": self.cuisine,
            "halal_status": self.halal_status,
            "image_url": self.image_url
        }