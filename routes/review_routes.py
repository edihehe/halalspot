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
    Then saves the review and redirects back to the restaurant page.
    """
    rating = request.form.get("rating")
    comment = request.form.get("comment", "")

    # Basic validation: ensure rating provided and between 1 and 5
    try:
        rating_int = int(rating)
        if rating_int < 1 or rating_int > 5:
            raise ValueError("Rating must be 1-5")
    except Exception:
        # For simplicity we ignore flash messaging in templates; redirect back.
        return redirect(url_for("restaurants.get_restaurant", id=id))

    review = Review(
        restaurant_id=id,
        rating=rating_int,
        comment=comment
    )

    db.session.add(review)
    db.session.commit()

    return redirect(url_for("restaurants.get_restaurant", id=id))