import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')  # Use SQLite by default
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'd0cac021bd7c0c95d4ff26336bbe05621681328286059234f30f0426a02b633d')  # Change this to a secure key
    DEBUG_METRICS=True