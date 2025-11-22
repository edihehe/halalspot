"""
utils/db.py

We keep a single db instance here and import it anywhere we need it.
This avoids circular import problems that commonly occur when models
and the app try to import each other.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()