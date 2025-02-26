import pytest
from app import create_app, db

@pytest.fixture
def app():
    # Create the Flask app with test configuration
    app = create_app(test_config={
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'TESTING': True,
        'JWT_SECRET_KEY': 'test-secret-key'  # Add JWT secret key for testing
    })
    
    # Set up the application context and database
    with app.app_context():
        db.create_all()  # Create all database tables
        yield app        # Yield the app for testing
        db.drop_all()    # Drop all database tables after testing

@pytest.fixture
def client(app):
    # Create a test client for making requests
    return app.test_client()