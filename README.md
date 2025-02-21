# **User Management Microservice Tutorial Series**

Welcome to the **User Management Microservice Tutorial Series**! In this series, we’ll build a production-ready microservice using **Flask** and **SQLAlchemy**. Each part of the series focuses on a specific aspect of the application, from setup to deployment.

---

## **Part 1: Setting Up the Project**

In **Part 1**, we set up the foundation for our microservice. Here’s what we covered:

### **What You’ll Learn in Part 1**
- How to set up a Python project with Flask and SQLAlchemy.
- How to structure your project for scalability.
- How to configure a SQLite database for development.
- How to run your Flask application locally.

---

### **Step-by-Step Guide for Part 1**

#### **Step 1: Create a Project Directory**
Start by creating a directory for your project:
```bash
mkdir user-management-microservice
cd user-management-microservice
```

#### **Step 2: Set Up a Virtual Environment**
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

#### **Step 3: Install Required Packages**
Install the necessary Python packages using `pip`:
```bash
pip install Flask SQLAlchemy Flask-SQLAlchemy
```

Here’s what each package does:
- **Flask**: A lightweight web framework for building APIs.
- **SQLAlchemy**: An ORM (Object-Relational Mapping) tool for database interactions.
- **Flask-SQLAlchemy**: Integrates SQLAlchemy with Flask.

#### **Step 4: Create the Project Structure**
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

#### **Step 5: Write the Configuration File**
Create a `config.py` file to store your application’s configuration:
```python
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')  # Use SQLite by default
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking
```

#### **Step 6: Initialize the Flask Application**
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

#### **Step 7: Define the Database Model**
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

#### **Step 8: Add a Basic Route**
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

#### **Step 9: Create the Entry Point**
In `run.py`, create the entry point to run the application:
```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

#### **Step 10: Run the Application**
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

## **Part 3: Completing CRUD Operations with JWT Authentication**

In **Part 3**, we’ll complete the **CRUD operations** for the `User` model and secure them using **JWT authentication**. Here’s what you’ll learn:

### **What’s Covered in Part 3**
1. **Implementing CRUD Operations**:
   - Fetch all users.
   - Fetch a single user by ID.
   - Update a user’s details.
   - Delete a user.

2. **Securing Endpoints with JWT Authentication**:
   - Protect routes using JWT tokens.
   - Implement a login endpoint to generate tokens.

3. **Testing the Endpoints**:
   - Test the CRUD operations and authentication using `curl` or Postman.

---

### **Step-by-Step Guide for Part 3**

#### **Step 1: Install Flask-JWT-Extended**

We’ll use the `Flask-JWT-Extended` library to handle JWT authentication. Install it using `pip`:

```bash
pip install flask-jwt-extended
```

#### **Step 2: Configure JWT in the Application**

Update `config.py` to include JWT configuration:

```python
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')  # Change this to a secure key
```

Update `app/__init__.py` to initialize JWT:
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

        db.create_all()

    return app
```

#### **Step 3: Implement the Login Endpoint**

In `app/routes.py`, add the login endpoint to generate JWT tokens:

```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from .models import User
from . import db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validate input
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username and password are required"}), 400

    username = data['username']
    password = data['password']

    # Find the user
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Generate a JWT token
        access_token = create_access_token(identity=str(user.id))  # Ensure identity is a string
        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Invalid credentials"}), 401
```

#### **Step 4: Complete CRUD Operations**

Let’s implement the remaining CRUD operations for the `User` model.

### **4.1: Fetch All Users**

Add a route to fetch all users:

```python
from flask_jwt_extended import jwt_required

@bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    users = User.query.all()
    return jsonify([{
        "id": user.id,
        "username": user.username,
        "email": user.email
    } for user in users])
```

### **4.2: Fetch a Single User**

Add a route to fetch a single user by ID:

```python
@bp.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })
```

### **4.3: Update a User**

Add a route to update a user’s details:

```python
@bp.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()

    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.set_password(data['password'])

    db.session.commit()
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })
```

### **4.4: Delete a User**

Add a route to delete a user:

```python
@bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})
```

#### **Step 5: Test the Endpoints**

Let’s test the CRUD endpoints using `curl` or Postman.

### **5.1: Log in to Get a JWT Token**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpass"}' http://127.0.0.1:5000/api/login
```

### **5.2: Fetch All Users**

```bash
curl -H "Authorization: Bearer <your-access-token>" http://127.0.0.1:5000/api/users
```

### **5.3: Fetch a Single User**

```bash
curl -H "Authorization: Bearer <your-access-token>" http://127.0.0.1:5000/api/users/1
```

### **5.4: Update a User**

```bash
curl -X PUT -H "Authorization: Bearer <your-access-token>" -H "Content-Type: application/json" -d '{"username": "updateduser"}' http://127.0.0.1:5000/api/users/1
```

### **5.5: Delete a User**

```bash
curl -X DELETE -H "Authorization: Bearer <your-access-token>" http://127.0.0.1:5000/api/users/1
```

---

## **What’s Next?**
In **Part 4**, we’ll add **error handling** and **input validation** to make the application more robust. Stay tuned!

---

## **Summary**

In this tutorial, we:

1. Installed and configured `Flask-JWT-Extended` for JWT authentication.
2. Implemented a login endpoint to generate JWT tokens.
3. Completed CRUD operations for the `User` model.
4. Secured all endpoints using JWT authentication.
5. Tested the endpoints using `curl`.

You now have a fully functional user management system! In the next part, we’ll improve error handling and input validation.

---

Let me know if you have any questions or need further assistance! 🚀

---
