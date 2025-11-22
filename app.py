"""
app.py

Application factory and app runner.
- creates Flask app
- configures database
- registers blueprints (route groups)
- ensures DB tables are created and inserts two mock restaurants if empty
"""

from flask import Flask, render_template
from config import Config
from utils.db import db

# Import blueprints after db is defined (they import models that import db)
from routes.restaurant_routes import restaurant_bp
from routes.review_routes import review_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize db with this app
    db.init_app(app)

    # Register our route blueprints
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(review_bp)

    # simple home route
    @app.route("/")
    def home():
        return render_template("home.html")

    return app


# --------------------------
# Helpers: insert demo data
# --------------------------
from models.restaurant import Restaurant

def insert_mock_data(app):
    """
    Insert two mock restaurants into the DB if none exist.
    Keeps the demo friendly for first-time runs.
    """
    with app.app_context():
        if Restaurant.query.count() == 0:
            r1 = Restaurant(
                name="Bismillah Grill",
                description="Authentic Pakistani & Indian halal food with fresh naan.",
                address="123 Halal Street, NY",
                latitude=40.7128,
                longitude=-74.0060,
                cuisine="Pakistani",
                halal_status="Certified Halal",
                image_url="/static/images/restaurant1.jpg"  # local placeholder
            )

            r2 = Restaurant(
                name="Medina Shawarma House",
                description="Halal Mediterranean shawarma, kebabs, and falafel.",
                address="55 Olive Road, NY",
                latitude=40.7132,
                longitude=-74.0025,
                cuisine="Mediterranean",
                halal_status="Muslim Owned",
                image_url="/static/images/restaurant2.jpg"
            )

            db.session.add_all([r1, r2])
            db.session.commit()


if __name__ == "__main__":
    app = create_app()
    # Create DB tables and insert demo data
    with app.app_context():
        db.create_all()
        insert_mock_data(app)

    # Start dev server
    app.run(debug=True)