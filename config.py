"""
config.py

Simple configuration holder. You can expand this later for
different environments (development, production, testing).
"""
import os
import secrets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    # Secret key for Flask sessions and flash messages
    # In production, use a strong, randomly generated secret key from environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    
    # SQLite file located inside the project folder
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'halalyelp.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False