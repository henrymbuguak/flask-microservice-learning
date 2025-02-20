# **Part 1: Setting Up the Project**

Welcome to **Part 1** of the tutorial series: **"Build a Production-Ready User Management Microservice with Flask and SQLAlchemy: A Step-by-Step Guide"**. In this part, we’ll set up the foundation for our **User Management Microservice**. By the end of this tutorial, you’ll have a basic Flask application with SQLAlchemy configured, ready for adding features like user registration, authentication, and more.

---

## **What You’ll Learn in Part 1**
- How to set up a Python project with Flask and SQLAlchemy.
- How to structure your project for scalability.
- How to configure a SQLite database for development.
- How to run your Flask application locally.

---

## **Prerequisites**
Before we begin, ensure you have the following installed:
- **Python 3.7+**: Download and install Python from [python.org](https://www.python.org/).
- **pip**: Python’s package manager (comes pre-installed with Python).
- **Basic knowledge of Python**: Familiarity with Python syntax and concepts will be helpful.

---

## **Step 1: Create a Project Directory**
Start by creating a directory for your project:
```bash
mkdir user-management-microservice
cd user-management-microservice
```

---

## **Step 2: Set Up a Virtual Environment**
A virtual environment isolates your project dependencies from the global Python installation. Create and activate a virtual environment:

### **On macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### **On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

Once activated, your terminal prompt will show the virtual environment name (`venv`).

---

## **Step 3: Install Required Packages**
Install the necessary Python packages using `pip`:
```bash
pip install Flask SQLAlchemy Flask-SQLAlchemy
```

Here’s what each package does:
- **Flask**: A lightweight web framework for building APIs.
- **SQLAlchemy**: An ORM (Object-Relational Mapping) tool for database interactions.
- **Flask-SQLAlchemy**: Integrates SQLAlchemy with Flask.

---

## **Step 4: Create the Project Structure**
Organize your project with the following structure:
```
user-management-microservice/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
├── config.py
├── run.py
├── requirements.txt
```

### **File Descriptions**
1. **`app/__init__.py`**: Initializes the Flask app and SQLAlchemy.
2. **`app/models.py`**: Defines the database models (e.g., `User`).
3. **`app/routes.py`**: Contains the API routes (e.g., `/api/users`).
4. **`config.py`**: Stores configuration settings (e.g., database URL).
5. **`run.py`**: Entry point to run the application.
6. **`requirements.txt`**: Lists the project dependencies.

---

## **Step 5: Write the Configuration File**
Create a `config.py` file to store your application’s configuration:
```python
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')  # Use SQLite by default
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking
```

---

## **Step 6: Initialize the Flask Application**
In `app/__init__.py`, initialize the Flask app and SQLAlchemy:
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        # Import and register routes
        from . import routes
        app.register_blueprint(routes.bp)

        # Create database tables
        db.create_all()

    return app
```

---

## **Step 7: Define the Database Model**
In `app/models.py`, define the `User` model:
```python
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
```

---

## **Step 8: Add a Basic Route**
In `app/routes.py`, create a simple route to test the setup:
```python
from flask import Blueprint, jsonify

# Create a Blueprint for the API routes
bp = Blueprint('api', __name__, url_prefix='/api')

# Define a simple test route
@bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Welcome to the User Management Microservice!"})
```

---

## **Step 9: Create the Entry Point**
In `run.py`, create the entry point to run the application:
```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

---

## **Step 10: Run the Application**
Start the application by running:
```bash
python run.py
```

You should see output similar to:
```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Visit `http://127.0.0.1:5000/api/test` in your browser or use `curl`:
```bash
curl http://127.0.0.1:5000/api/test
```

You should see the following response:
```json
{
  "message": "Welcome to the User Management Microservice!"
}
```

---

## **Part 2: User Registration and Database Models**

In **Part 2**, we dive into designing the **User model**, implementing **user registration**, and securing passwords using **Werkzeug**. Here’s what you’ll learn:

### **What’s Covered in Part 2**
1. **Designing the User Model**:
   - Added fields for `username`, `email`, and `password_hash`.
   - Implemented password hashing using Werkzeug.

2. **Implementing User Registration**:
   - Created a `/api/register` endpoint for user registration.
   - Added input validation and duplicate checks.

3. **Testing the Registration Endpoint**:
   - Tested the endpoint using `curl` and Postman.
   - Verified the database to ensure data is stored correctly.

### **Code Example**
#### **User Model (`app/models.py`)**
```python
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
```

#### **Registration Endpoint (`app/routes.py`)**
```python
from flask import Blueprint, request, jsonify
from .models import User
from . import db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate input
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Username, email, and password are required"}), 400

    # Check if the username or email already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400

    # Create a new user
    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])  # Hash the password
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }), 201
```

### **Testing the Endpoint**
#### **Using `curl`**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "email": "test@example.com", "password": "testpass"}' http://127.0.0.1:5000/api/register
```

#### **Expected Response**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com"
}
```

---

## **What’s Next?**
In **Part 3**, we’ll implement **user authentication** using JSON Web Tokens (JWT). Stay tuned!

---

Let me know if you have any questions or need further assistance! 🚀