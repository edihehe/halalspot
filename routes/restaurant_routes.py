"""
routes/restaurant_routes.py

Handles views for:
- listing all restaurants
- search results
- single restaurant details
- map page
"""

from flask import Blueprint, request, render_template
from models.restaurant import Restaurant
from models.review import Review

restaurant_bp = Blueprint("restaurants", __name__)

@restaurant_bp.route("/restaurants")
def list_restaurants():
    """
    Shows all restaurants. In a larger app you would paginate results.
    """
    restaurants = Restaurant.query.all()
    return render_template("search.html", restaurants=restaurants)

@restaurant_bp.route("/restaurants/<int:id>")
def get_restaurant(id):
    """
    Restaurant detail page.
    Loads the restaurant and its reviews.
    """
    restaurant = Restaurant.query.get_or_404(id)
    # Fetch reviews associated with this restaurant
    reviews = Review.query.filter_by(restaurant_id=id).order_by(Review.date.desc()).all()
    return render_template("restaurant.html", restaurant=restaurant, reviews=reviews)

@restaurant_bp.route("/restaurants/search")
def search_restaurants():
    """
    Basic search by name (case-insensitive contains).
    For production, use a proper full-text search or indexed fields.
    """
    query = request.args.get("query", "")
    if query:
        results = Restaurant.query.filter(Restaurant.name.ilike(f"%{query}%")).all()
    else:
        results = []
    return render_template("search.html", restaurants=results, query=query)

@restaurant_bp.route("/restaurants/map")
def show_map():
    """
    Map view that shows all restaurants as markers.
    Convert Restaurant objects to dicts before passing to template.
    """
    restaurants = Restaurant.query.all()
    # Convert SQLAlchemy objects to dicts for JSON serialization
    restaurants_dicts = [r.to_dict() for r in restaurants]
    return render_template("map.html", restaurants=restaurants_dicts)