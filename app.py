"""
app.py

Application factory and app runner.
- creates Flask app
- configures database
- registers blueprints (route groups)
- ensures DB tables are created and inserts demo restaurants if empty
"""

from flask import Flask, render_template
from config import Config
from utils.db import db

# Import blueprints after db is defined (they import models that import db)
from routes.restaurant_routes import restaurant_bp
from routes.review_routes import review_bp
from models.restaurant import Restaurant


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize db with this app
    db.init_app(app)

    # Register route blueprints
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(review_bp)
    
    # --------------------------
    # Home route with restaurants
    # --------------------------
    @app.route("/")
    def home():
        # Query all restaurants and convert to dicts for JSON serialization
        restaurants = [r.to_dict() for r in Restaurant.query.all()]
        return render_template("home.html", restaurants=restaurants)

    return app



# --------------------------
# Insert demo Philly restaurants
# --------------------------
def insert_demo_restaurants(app):
    """
    Insert demo Philly restaurants into the DB if none exist.
    Update this list with the real restaurants you want to display.
    """
    demo_restaurants = [
        {
            "name": "Halal Guys Philly",
            "description": "Authentic Mediterranean & Middle Eastern halal dishes.",
            "address": "123 Chestnut St, Philadelphia, PA",
            "latitude": 39.9496,
            "longitude": -75.1503,
            "cuisine": "Mediterranean",
            "halal_status": "Certified Halal",
            "image_url": "/static/images/r1.jpg"
        },
        {
            "name": "Philly Shawarma",
            "description": "Halal Middle Eastern shawarma, falafel & more.",
            "address": "456 Market St, Philadelphia, PA",
            "latitude": 39.9502,
            "longitude": -75.1457,
            "cuisine": "Middle Eastern",
            "halal_status": "Muslim Owned",
            "image_url": "/static/images/r2.jpg"
        },
        {
            "name": "Mediterraneo Philly",
            "description": "Halal Mediterranean dishes, kebabs & falafel.",
            "address": "789 Walnut St, Philadelphia, PA",
            "latitude": 39.9521,
            "longitude": -75.1450,
            "cuisine": "Mediterranean",
            "halal_status": "Certified Halal",
            "image_url": "/static/images/r3.jpg"
        },
        {
            "name": "Halal Grill Express",
            "description": "Fast casual halal meals including gyros and rice plates.",
            "address": "321 Broad St, Philadelphia, PA",
            "latitude": 39.9508,
            "longitude": -75.1555,
            "cuisine": "Middle Eastern",
            "halal_status": "Muslim Owned",
            "image_url": "/static/images/r4.jpg"
        },
        {
            "name": "Phoenicia Halal",
            "description": "Halal Lebanese & Mediterranean cuisine with fresh ingredients.",
            "address": "654 Arch St, Philadelphia, PA",
            "latitude": 39.9515,
            "longitude": -75.1483,
            "cuisine": "Lebanese",
            "halal_status": "Certified Halal",
            "image_url": "/static/images/r5.jpg"
        },
    ]

    with app.app_context():
        if Restaurant.query.count() == 0:
            for r in demo_restaurants:
                restaurant = Restaurant(
                    name=r["name"],
                    description=r["description"],
                    address=r["address"],
                    latitude=r["latitude"],
                    longitude=r["longitude"],
                    cuisine=r["cuisine"],
                    halal_status=r["halal_status"],
                    image_url=r["image_url"]
                )
                db.session.add(restaurant)
            db.session.commit()
            print(f"Inserted {len(demo_restaurants)} demo restaurants.")


# --------------------------
# Run app
# --------------------------
if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()              # create tables if not exist
        insert_demo_restaurants(app) # insert Philly restaurants if empty

    app.run(debug=True)