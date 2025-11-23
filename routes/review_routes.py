"""
routes/review_routes.py

Handles anonymous review submission.
No authentication; reviews are immediately saved and shown on the restaurant page.
"""

from flask import Blueprint, request, redirect, url_for, flash
from models.review import Review
from models.restaurant import Restaurant
from utils.db import db

review_bp = Blueprint("reviews", __name__)

@review_bp.route("/restaurants/<int:id>/reviews/add", methods=["POST"])
def add_review(id):
    """
    Accepts form data:
    - rating (int)
    - comment (text)
    Saves the review and redirects back to the restaurant page.
    """
    
    # Verify restaurant exists
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        flash("Restaurant not found.", "error")
        return redirect(url_for("restaurants.list_restaurants"))

    # Get form data
    rating = request.form.get("rating")
    comment = request.form.get("comment", "").strip()  # remove extra spaces

    # Validate rating - check if it exists and is not empty
    if not rating or (isinstance(rating, str) and rating.strip() == ""):
        flash("Please select a rating.", "error")
        return redirect(url_for("restaurants.get_restaurant", id=id))
    
    # Validate rating
    try:
        rating_int = int(rating)
        if rating_int < 1 or rating_int > 5:
            raise ValueError("Rating must be 1-5")
    except (ValueError, TypeError):
        flash("Invalid rating. Please submit a number between 1 and 5.", "error")
        return redirect(url_for("restaurants.get_restaurant", id=id))

    # Optional: Validate comment length
    if len(comment) > 500:
        flash("Comment too long (max 500 characters).", "error")
        return redirect(url_for("restaurants.get_restaurant", id=id))

    # Create and save the review
    try:
        review = Review(
            restaurant_id=id,
            rating=rating_int,
            comment=comment if comment else None
        )
        db.session.add(review)
        db.session.commit()
        flash("Review added successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error saving review: {str(e)}", "error")
        # Log the error for debugging (in production, use proper logging)
        print(f"Error saving review: {e}")
    
    return redirect(url_for("restaurants.get_restaurant", id=id))