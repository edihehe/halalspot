# reset_restaurants.py

from app import create_app
from utils.db import db
from models.restaurant import Restaurant

app = create_app()

with app.app_context():
    # Delete all old restaurants
    num_deleted = db.session.query(Restaurant).delete()
    db.session.commit()
    print(f"Deleted {num_deleted} old restaurants.")