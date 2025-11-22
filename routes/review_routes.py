"""
routes/review_routes.py

Handles anonymous review submission.
No authentication; reviews are immediately saved and shown on the restaurant page.
"""

from flask import Blueprint, request, redirect, url_for, flash
from models.review import Review
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

    # Get form data
    rating = request.form.get("rating")
    comment = request.form.get("comment", "").strip()  # remove extra spaces

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
    review = Review(
        restaurant_id=id,
        rating=rating_int,
        comment=comment
    )
    db.session.add(review)
    db.session.commit()

    flash("Review added successfully!", "success")
    return redirect(url_for("restaurants.get_restaurant", id=id))