import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')  # Use SQLite by default
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')  # Change this to a secure key