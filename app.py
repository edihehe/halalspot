"""
app.py

Application factory and app runner.
- creates Flask app
- configures database
- registers blueprints (route groups)
- ensures DB tables are created and inserts demo restaurants if empty
"""

from flask import Flask, render_template, request, redirect, url_for
from config import Config
from utils.db import db

# Import blueprints after db is defined (they import models that import db)
from routes.restaurant_routes import restaurant_bp
from routes.review_routes import review_bp
from routes.fyp_routes import fyp_bp
from models.restaurant import Restaurant
from models.content import Content

def insert_demo_restaurants(app):

    demo_restaurants = [
        {
            "name": "The Halal Guys",
            "description": "Famous for gyro platters, chicken over rice, and white & red sauce — a well-known halal street-food chain.",
            "address": "37 E City Ave, Bala Cynwyd, PA 19004",
            "latitude": 40.002599,
            "longitude": -75.225074,
            "cuisine": "Middle Eastern",
            "halal_status": "Certified Halal",
            "image_url": "/static/images/halalGuy.png",
        },
        {
            "name": "Dave's Hot Chicken",
            "description": "Famous halal-certified hot chicken tenders and sliders served with bold spice levels.",
            "address": "1731 Chestnut St, Philadelphia, PA 19103",
            "latitude": 39.951923,
            "longitude": -75.169856,
            "cuisine": "American",
            "halal_status": "Certified Halal",
            "image_url": "/static/images/daves.jpg",
        },
        {
            "name": "Crown Fried Chicken",
            "description": "Classic halal fried chicken spot offering crispy chicken, sandwiches, and late-night comfort food.",
            "address": "600 S Broad St, Philadelphia, PA 19146",
            "latitude": 39.943588,
            "longitude": -75.165840,
            "cuisine": "American",
            "halal_status": "Halal",
            "image_url": "/static/images/crown.png",
        },
        {
            "name": "Asad's Hot Chicken",
            "description": "Nashville-style halal hot chicken known for crispy spice levels and fresh sides.",
            "address": "4627 Woodland Ave, Philadelphia, PA 19143",
            "latitude": 39.943994,
            "longitude": -75.210697,
            "cuisine": "American",
            "halal_status": "Halal",
            "image_url": "/static/images/asad.png",
        },
        {
            "name": "Saad's Halal Restaurant",
            "description": "West Philly staple serving shawarma, falafel, platters, and cheesesteaks — all 100% halal.",
            "address": "4500 Walnut St, Philadelphia, PA 19139",
            "latitude": 39.9550021,
            "longitude": -75.2118988,
            "cuisine": "Middle Eastern",
            "halal_status": "Certified Halal",
            "image_url": "/static/images/saad.png",
        },
        {
            "name": "Pasha's Halal Food",
            "description": "Temple-famous halal platters, gyros, and wraps brought from the food truck to a brick-and-mortar spot.",
            "address": "1652 N 2nd St, Philadelphia, PA 19122",
            "latitude": 39.9761172,
            "longitude": -75.1383489,
            "cuisine": "Middle Eastern",
            "halal_status": "Halal",
            "image_url": "/static/images/pashas.jpg",
        },
        {
            "name": "Manakeesh Cafe Bakery & Grill",
            "description": "Lebanese bakery and cafe known for fresh flatbreads, shawarma, and a big selection of sweets.",
            "address": "4420 Walnut St, Philadelphia, PA 19104",
            "latitude": 39.9550873,
            "longitude": -75.2115307,
            "cuisine": "Lebanese",
            "halal_status": "Halal",
            "image_url": "/static/images/manakeesh.jpg",
        },
        {
            "name": "Doro Bet",
            "description": "Ethiopian-inspired fried chicken spot with halal-friendly chicken, bold spices, and gluten-free batter.",
            "address": "4533 Baltimore Ave, Philadelphia, PA 19143",
            "latitude": 39.9491177,
            "longitude": -75.2144112,
            "cuisine": "Ethiopian / Fried Chicken",
            "halal_status": "Halal-Friendly",
            "image_url": "/static/images/dorobet.jpg",
        },
        {
            "name": "Kabobeesh",
            "description": "Popular Pakistani grill known for BBQ, kabobs, naan, and homestyle curries — all halal.",
            "address": "4201 Chestnut St, Philadelphia, PA 19104",
            "latitude": 39.9565219,
            "longitude": -75.2069933,
            "cuisine": "Pakistani",
            "halal_status": "Halal",
            "image_url": "/static/images/kabobeesh.jpg",
        },
        {
            "name": "Halal Fusionz",
            "description": "Halal smash burgers, wings, tenders, and fries with Philly-fusion flavors.",
            "address": "2516 Federal St, Philadelphia, PA 19146",
            "latitude": 39.9384975,
            "longitude": -75.1859752,
            "cuisine": "American / Fusion",
            "halal_status": "Halal",
            "image_url": "/static/images/halalfusionz.jpg",
        },
        {
            "name": "Sahara Indian Cuisine",
            "description": "Indian-Pakistani halal restaurant serving biryani, tandoori, curries, and lunch specials.",
            "address": "531 S 52nd St, Philadelphia, PA 19143",
            "latitude": 39.951154,
            "longitude": -75.226609,
            "cuisine": "Indian / Pakistani",
            "halal_status": "Halal",
            "image_url": "/static/images/sahara.jpg",
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
                    image_url=r["image_url"],
                )
                db.session.add(restaurant)
            db.session.commit()
            print(f"Inserted {len(demo_restaurants)} demo restaurants.")

def insert_demo_content(app):
    """Insert demo content for FYP feed"""
    with app.app_context():
        if Content.query.count() == 0:
            restaurants = Restaurant.query.all()
            
            demo_content = [
                {
                    "restaurant_id": restaurants[0].id if restaurants else None,
                    "title": "🔥 Halal Guys Gyro Platter",
                    "description": "The most iconic halal street food in Philly! White sauce, red sauce, and perfectly seasoned chicken over rice. A must-try! 🍗✨",
                    "image_url": "/static/images/halalGuy.png",
                    "video_url": "/static/videos/halalguys.mp4",
                    "likes_count": 1247,
                    "comments_count": 89,
                    "shares_count": 234,
                    "saves_count": 156,
                    "order_url": f"/restaurants/{restaurants[0].id}" if restaurants else None
                },
                {
                    "restaurant_id": restaurants[3].id if len(restaurants) > 3 else None,
                    "title": "Nashville Hot Chicken",
                    "description": "Asad's Hot Chicken bringing the heat! 🌶️ Nashville-style halal chicken that's absolutely fire!",
                    "image_url": "/static/images/asad.png",
                    "video_url": "/static/videos/asads.mp4",
                    "likes_count": 1123,
                    "comments_count": 78,
                    "shares_count": 189,
                    "saves_count": 134,
                    "order_url": f"/restaurants/{restaurants[3].id}" if len(restaurants) > 3 else None
                },
                {
                    "restaurant_id": restaurants[4].id if len(restaurants) > 4 else None,
                    "title": "Shawarma Platter",
                    "description": "Saad's Halal Restaurant serving up authentic shawarma! 🥙 Fresh, flavorful, and always halal certified.",
                    "image_url": "/static/images/saad.png",
                    "video_url": "/static/videos/saads.mp4",
                    "likes_count": 987,
                    "comments_count": 56,
                    "shares_count": 145,
                    "saves_count": 112,
                    "order_url": f"/restaurants/{restaurants[4].id}" if len(restaurants) > 4 else None
                },
                {
                    "creator_name": "HalalFoodie_Philly",
                    "is_sponsored": True,
                    "title": "Hidden Gem: Best Halal Spot in West Philly",
                    "description": "Just discovered this amazing spot! The shawarma here is incredible and the prices are unbeatable. Definitely check it out! 🎯",
                    "image_url": "/static/images/saad.png",
                    "video_url": "/static/videos/IMG_4123.mp4",
                    "likes_count": 2341,
                    "comments_count": 156,
                    "shares_count": 289,
                    "saves_count": 445,
                    "order_url": None
                }
            ]
            
            for c in demo_content:
                content = Content(
                    restaurant_id=c.get("restaurant_id"),
                    creator_name=c.get("creator_name"),
                    is_sponsored=c.get("is_sponsored", False),
                    title=c["title"],
                    description=c["description"],
                    image_url=c.get("image_url"),  # Keep as poster/thumbnail
                    video_url=c.get("video_url"),  # Add video URL
                    likes_count=c["likes_count"],
                    comments_count=c["comments_count"],
                    shares_count=c["shares_count"],
                    saves_count=c["saves_count"],
                    order_url=c.get("order_url")
                )
                db.session.add(content)
            
            db.session.commit()
            print(f"Inserted {len(demo_content)} demo content posts.")

# --------------------------
# Create Flask app
# --------------------------
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize db with this app
    db.init_app(app)

    # Register route blueprints
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(fyp_bp)

    # --------------------------
    # Home route
    # --------------------------
    @app.route("/")
    def home():
        restaurants = [r.to_dict() for r in Restaurant.query.all()]

         # Attach average rating if reviews exist
        for r in restaurants:
            reviews = review_store.get(r["id"], [])
            if reviews:
                avg = sum([rev["rating"] for rev in reviews]) / len(reviews)
                r["avg_rating"] = round(avg, 1)
            else:
                r["avg_rating"] = None

        return render_template("home.html", restaurants=restaurants)

    # --------------------------
    # Contact route
    # --------------------------
    @app.route("/contact")
    def contact():
        return render_template("contact.html")

    # In-memory review store
    review_store = {}

    @app.route("/reviews", methods=["GET", "POST"])
    def reviews():
        restaurants = [r.to_dict() for r in Restaurant.query.all()]

        if request.method == "POST":
            restaurant_id = request.form.get("restaurant_id")
            review_text = (request.form.get("review_text") or "").strip()
            rating = request.form.get("rating")

            if restaurant_id and review_text and rating:
                restaurant_id = int(restaurant_id)
                rating = int(rating)

                if restaurant_id not in review_store:
                    review_store[restaurant_id] = []
                review_store[restaurant_id].append({"text": review_text, "rating": rating})

            return redirect(url_for("reviews"))

        # Attach reviews and average rating
        for r in restaurants:
            reviews = review_store.get(r["id"], [])
            r["reviews"] = reviews
            if reviews:
                avg = sum([rev["rating"] for rev in reviews]) / len(reviews)
                r["avg_rating"] = round(avg, 1)
            else:
                r["avg_rating"] = None
        return render_template("reviews.html", restaurants=restaurants)






    # --------------------------
    # Search route
    # --------------------------
    @app.route("/find", methods=["GET"])
    def find():
        query = request.args.get("query", "").strip().lower()
        restaurants = [r.to_dict() for r in Restaurant.query.all()]

        if query:
            filtered = [
                r for r in restaurants
                if query in r["name"].lower()
                or query in r["cuisine"].lower()
                or query in r["description"].lower()
            ]
        else:
            filtered = restaurants

        return render_template(
            "home.html",
            restaurants=filtered,
            query=query
        )
    return app

# --------------------------
# Run app
# --------------------------
if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()  # Create tables if they don't exist
        insert_demo_restaurants(app)  # Insert demo restaurants if empty
        insert_demo_content(app)  # Insert demo content if empty

    app.run(debug=True)