"""
config.py

Simple configuration holder. You can expand this later for
different environments (development, production, testing).
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    # SQLite file located inside the project folder
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'halalyelp.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False