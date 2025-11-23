"""
routes/fyp_routes.py

Handles FYP (For You Page) routes for food content feed.
"""

from flask import Blueprint, request, jsonify, render_template
from models.content import Content, ContentComment
from models.restaurant import Restaurant
from utils.db import db
import json

fyp_bp = Blueprint("fyp", __name__)

@fyp_bp.route("/fyp")
def fyp_page():
    """Main FYP page"""
    contents = Content.query.order_by(Content.created_at.desc()).all()
    contents_data = [c.to_dict() for c in contents]
    
    # Attach restaurant info if available
    for content in contents_data:
        if content["restaurant_id"]:
            restaurant = Restaurant.query.get(content["restaurant_id"])
            if restaurant:
                content["restaurant"] = restaurant.to_dict()
    
    return render_template("fyp.html", contents=contents_data)

@fyp_bp.route("/api/fyp/content", methods=["GET"])
def get_content():
    """API endpoint to get all content"""
    contents = Content.query.order_by(Content.created_at.desc()).all()
    contents_data = [c.to_dict() for c in contents]
    
    # Attach restaurant info
    for content in contents_data:
        if content["restaurant_id"]:
            restaurant = Restaurant.query.get(content["restaurant_id"])
            if restaurant:
                content["restaurant"] = restaurant.to_dict()
    
    return jsonify(contents_data)

@fyp_bp.route("/api/fyp/content/<int:content_id>/like", methods=["POST"])
def like_content(content_id):
    """Toggle like on content"""
    content = Content.query.get_or_404(content_id)
    data = request.get_json() or {}
    action = data.get("action", "toggle")  # "like" or "unlike"
    
    if action == "like":
        content.likes_count += 1
    elif action == "unlike" and content.likes_count > 0:
        content.likes_count -= 1
    
    db.session.commit()
    return jsonify({"success": True, "likes_count": content.likes_count})

@fyp_bp.route("/api/fyp/content/<int:content_id>/comment", methods=["POST"])
def add_comment(content_id):
    """Add a comment to content"""
    content = Content.query.get_or_404(content_id)
    data = request.get_json() or {}
    
    comment_text = data.get("comment_text", "").strip()
    username = data.get("username", "Anonymous").strip() or "Anonymous"
    
    if not comment_text:
        return jsonify({"success": False, "error": "Comment text is required"}), 400
    
    comment = ContentComment(
        content_id=content_id,
        username=username,
        comment_text=comment_text
    )
    db.session.add(comment)
    content.comments_count += 1
    db.session.commit()
    
    return jsonify({
        "success": True,
        "comment": comment.to_dict(),
        "comments_count": content.comments_count
    })

@fyp_bp.route("/api/fyp/content/<int:content_id>/comments", methods=["GET"])
def get_comments(content_id):
    """Get all comments for a content"""
    comments = ContentComment.query.filter_by(content_id=content_id).order_by(ContentComment.created_at.desc()).all()
    return jsonify([c.to_dict() for c in comments])

@fyp_bp.route("/api/fyp/content/<int:content_id>/share", methods=["POST"])
def share_content(content_id):
    """Increment share count"""
    content = Content.query.get_or_404(content_id)
    content.shares_count += 1
    db.session.commit()
    return jsonify({"success": True, "shares_count": content.shares_count})

@fyp_bp.route("/api/fyp/content/<int:content_id>/save", methods=["POST"])
def save_content(content_id):
    """Toggle save on content"""
    content = Content.query.get_or_404(content_id)
    data = request.get_json() or {}
    action = data.get("action", "toggle")
    
    if action == "save":
        content.saves_count += 1
    elif action == "unsave" and content.saves_count > 0:
        content.saves_count -= 1
    
    db.session.commit()
    return jsonify({"success": True, "saves_count": content.saves_count})

@fyp_bp.route("/api/fyp/content/<int:content_id>/order", methods=["POST"])
def order_from_content(content_id):
    """Handle order action - redirects to restaurant order page"""
    content = Content.query.get_or_404(content_id)
    
    if content.restaurant_id:
        restaurant = Restaurant.query.get(content.restaurant_id)
        if restaurant:
            # In a real app, this would integrate with ordering system
            # For now, return restaurant info
            return jsonify({
                "success": True,
                "restaurant_id": restaurant.id,
                "restaurant_name": restaurant.name,
                "order_url": content.order_url or f"/restaurants/{restaurant.id}"
            })
    
    return jsonify({"success": False, "error": "No restaurant associated"}), 400

