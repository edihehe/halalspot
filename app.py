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

    @app.route("/contact")
    def contact():
        return render_template("contact.html")
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
    "name": "The Halal Guys",
    "description": "Famous for gyro platters, chicken over rice, and white & red sauce — a well-known halal street-food chain.",
    "address": "37 E City Ave, Bala Cynwyd, PA 19004",
    "latitude": 40.002599,
    "longitude": -75.225074,
    "cuisine": "Middle Eastern",
    "halal_status": "Certified Halal",
    "image_url": "/static/images/halalGuy.png"
},
{
    "name": "Dave's Hot Chicken",
    "description": "Famous halal-certified hot chicken tenders and sliders served with bold spice levels.",
    "address": "1731 Chestnut St, Philadelphia, PA 19103",
    "latitude": 39.951923,
    "longitude": -75.169856,
    "cuisine": "American",
    "halal_status": "Certified Halal",
    "image_url": "/static/images/daves.jpg"
},
{
    "name": "Crown Fried Chicken",
    "description": "Classic halal fried chicken spot offering crispy chicken, sandwiches, and late-night comfort food.",
    "address": "600 S Broad St, Philadelphia, PA 19146",
    "latitude": 39.943588,
    "longitude": -75.165840,
    "cuisine": "American",
    "halal_status": "Halal",
    "image_url": "/static/images/crown.png"
},
{
    "name": "Asad's Hot Chicken",
    "description": "Nashville-style halal hot chicken known for crispy spice levels and fresh sides.",
    "address": "4627 Woodland Ave, Philadelphia, PA 19143",
    "latitude": 39.943994,
    "longitude": -75.210697,
    "cuisine": "American",
    "halal_status": "Halal",
    "image_url": "/static/images/asad.png"
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