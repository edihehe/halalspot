"""
models/content.py

Content model for FYP posts - food content from businesses and creators.
"""

import datetime
from utils.db import db

class Content(db.Model):
    __tablename__ = "content"

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=True)  # Can be null for creator posts
    creator_name = db.Column(db.String(255), nullable=True)  # For sponsored creators
    is_sponsored = db.Column(db.Boolean, default=False)
    
    # Content details
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    video_url = db.Column(db.String(255), nullable=True)  # For future video support
    
    # Engagement metrics
    likes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    shares_count = db.Column(db.Integer, default=0)
    saves_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Order link (for restaurant posts)
    order_url = db.Column(db.String(255), nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "restaurant_id": self.restaurant_id,
            "creator_name": self.creator_name,
            "is_sponsored": self.is_sponsored,
            "title": self.title,
            "description": self.description,
            "image_url": self.image_url,
            "video_url": self.video_url,
            "likes_count": self.likes_count,
            "comments_count": self.comments_count,
            "shares_count": self.shares_count,
            "saves_count": self.saves_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "order_url": self.order_url
        }

class ContentComment(db.Model):
    __tablename__ = "content_comment"
    
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    username = db.Column(db.String(100), default="Anonymous")
    comment_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "content_id": self.content_id,
            "username": self.username,
            "comment_text": self.comment_text,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

