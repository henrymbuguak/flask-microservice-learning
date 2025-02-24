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

## **Part 4: Error Handling and Input Validation**

In **Part 4**, we’ll enhance the application by adding **error handling** and **input validation**. Here’s what you’ll learn:

### **What’s Covered in Part 4**
1. **Global Error Handling**:
   - Handle common HTTP errors like 404 (Not Found) and 500 (Internal Server Error).
   - Return meaningful error messages to the client.

2. **Input Validation**:
   - Validate user input using `marshmallow`.
   - Ensure data integrity and prevent invalid data from entering the system.

3. **Testing Error Handling and Validation**:
   - Test error responses and validation using `curl` or Postman.

---

### **Step-by-Step Guide for Part 4**

#### **Step 1: Add Global Error Handling**
Add global error handlers to handle common HTTP errors.

### **Update `app/__init__.py`**
```python
from flask import jsonify

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    # Register error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found", "message": "The requested resource was not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal Server Error", "message": "Something went wrong on the server"}), 500

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

        db.create_all()

    return app
```

#### **Step 2: Add Input Validation**
Use `marshmallow` to validate user input for the `/api/register` and `/api/login` endpoints.

### **Install Marshmallow**
Install `marshmallow` using `pip`:
```bash
pip install marshmallow
```

### **Create a Validation Schema**
Create a new file `app/schemas.py` to define validation schemas:
```python
from marshmallow import Schema, fields, ValidationError

class UserSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

# Create an instance of the schema
user_schema = UserSchema()
```

### **Update the Registration Endpoint**
Update the `/api/register` endpoint in `app/routes.py` to use the validation schema:
```python
from .schemas import user_schema, ValidationError

@bp.route('/register', methods=['POST'])
def register():
    try:
        # Validate and deserialize the input data
        data = user_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": "Validation Error", "messages": err.messages}), 400

    # Check if the username or email already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400

    # Create a new user
    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }), 201
```

### **Update the Login Endpoint**
Update the `/api/login` endpoint in `app/routes.py` to use the validation schema:
```python
@bp.route('/login', methods=['POST'])
def login():
    try:
        # Validate and deserialize the input data
        data = user_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": "Validation Error", "messages": err.messages}), 400

    username = data['username']
    password = data['password']

    # Find the user
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Generate a JWT token
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Invalid credentials"}), 401
```

#### **Step 3: Test Error Handling and Validation**
Let’s test the error handling and validation using `curl` or Postman.

### **Test 404 Error**
Try accessing a non-existent endpoint:
```bash
curl http://127.0.0.1:5000/api/nonexistent
```

### **Expected Response**
```json
{
  "error": "Not Found",
  "message": "The requested resource was not found"
}
```

### **Test Validation Errors**
Send invalid data to the `/api/register` endpoint:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "email": "invalid-email", "password": "testpass"}' http://127.0.0.1:5000/api/register
```

### **Expected Response**
```json
{
  "error": "Validation Error",
  "messages": {
    "email": ["Not a valid email address."]
  }
}
```

---

## **Part 5: Logging and Monitoring – Tracking Requests and Performance in Your Microservice**

In **Part 5**, we’ll add **logging** and **monitoring** to the application to track requests, errors, and performance. Here’s what you’ll learn:

### **What You’ll Learn in Part 5**
- How to add logging to track requests, errors, and important events.
- How to configure log levels and log file rotation.
- How to set up **[Prometheus](https://prometheus.io/)** and **[Grafana](https://grafana.com/)** to monitor application performance.
- How to handle logging for Flask applications using the `@jwt_required` decorator.
- How to test logging and monitoring.

---

### **Step-by-Step Guide for Part 5**

#### **Step 1: Add Logging to the Application**
Logging helps track requests, errors, and important events in your application. Let’s configure logging in the Flask app.

### **Update `app/__init__.py`**
Add logging configuration to the `create_app` function:
```python
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    # Configure logging
    if not app.debug:
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.mkdir('logs')

        # Set up a rotating file handler
        file_handler = RotatingFileHandler(
            'logs/microservice.log', maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        # Set the log level for the application
        app.logger.setLevel(logging.INFO)
        app.logger.info('Microservice startup')

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

        db.create_all()

    return app
```

### **Explanation**
- **RotatingFileHandler**: Logs are written to `logs/microservice.log`, and the file rotates when it reaches 10 KB. Up to 10 backup files are kept.
- **Log Format**: Includes the timestamp, log level, message, and source file location.
- **Log Level**: Set to `INFO` for production. You can change it to `DEBUG` for more detailed logs during development.

---

#### **Step 2: Add Logging to Routes**
Add logging to the routes to track requests and errors.

### **Update `app/routes.py`**
Add logging to the `/api/register` and `/api/login` endpoints:
```python
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import User
from . import db
from .schemas import user_schema, ValidationError

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/register', methods=['POST'])
def register():
    try:
        # Validate and deserialize the input data
        data = user_schema.load(request.get_json())
    except ValidationError as err:
        current_app.logger.error(f"Validation error: {err.messages}")
        return jsonify({"error": "Validation Error", "messages": err.messages}), 400

    # Check if the username or email already exists
    if User.query.filter_by(username=data['username']).first():
        current_app.logger.warning(f"Username already exists: {data['username']}")
        return jsonify({"error": "Username already exists"}), 400
    if User.query.filter_by(email=data['email']).first():
        current_app.logger.warning(f"Email already exists: {data['email']}")
        return jsonify({"error": "Email already exists"}), 400

    # Create a new user
    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    current_app.logger.info(f"New user registered: {new_user.username}")
    return jsonify({
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    try:
        # Validate and deserialize the input data
        data = user_schema.load(request.get_json())
    except ValidationError as err:
        current_app.logger.error(f"Validation error: {err.messages}")
        return jsonify({"error": "Validation Error", "messages": err.messages}), 400

    username = data['username']
    password = data['password']

    # Find the user
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Generate a JWT token
        access_token = create_access_token(identity=str(user.id))
        current_app.logger.info(f"User logged in: {user.username}")
        return jsonify(access_token=access_token), 200

    current_app.logger.warning(f"Invalid login attempt for username: {username}")
    return jsonify({"error": "Invalid credentials"}), 401
```

### **Handling `@jwt_required` Decorator**
When using the `@jwt_required` decorator, you can log JWT-related events such as token validation failures or unauthorized access attempts. Here’s an example:

```python
@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        current_app.logger.warning(f"Unauthorized access attempt by user ID: {current_user_id}")
        return jsonify({"error": "User not found"}), 404

    current_app.logger.info(f"Authorized access by user: {user.username}")
    return jsonify({"message": f"Hello, {user.username}!"}), 200
```

---

#### **Step 3: Set Up Prometheus and Grafana**
Prometheus and Grafana are powerful tools for monitoring and visualizing application metrics. Here’s how to set them up.

### **Step 3.1: Install Docker (if not already installed)**

If you don’t have Docker installed, follow these steps to set it up:

#### **On Linux**
1. **Install Docker**:
   Run the following commands in your terminal:
   ```bash
   sudo apt-get update
   sudo apt-get install docker.io
   ```

2. **Start Docker**:
   Start the Docker service and enable it to run on boot:
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

3. **Verify Installation**:
   Check if Docker is installed correctly:
   ```bash
   docker --version
   ```

#### **On macOS**
1. **Download Docker Desktop**:
   - Go to the [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop) page.
   - Download and install Docker Desktop.

2. **Start Docker**:
   - Open Docker Desktop from your Applications folder.
   - Verify installation by running:
     ```bash
     docker --version
     ```

#### **On Windows**
1. **Download Docker Desktop**:
   - Go to the [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop) page.
   - Download and install Docker Desktop.

2. **Start Docker**:
   - Open Docker Desktop from your Start menu.
   - Verify installation by running in Command Prompt:
     ```cmd
     docker --version
     ```

---

### **Step 3.2: Create the `docker-compose.yml` File**

1. **Where to Place the File**:
   - Create a file named `docker-compose.yml` in the **root directory** of your project (the same folder where your Flask app’s main files are located).

2. **Add the Following Content**:
   ```yaml
   version: '3.7'

   services:
     prometheus:
       image: prom/prometheus
       container_name: prometheus
       ports:
         - "9090:9090"
       volumes:
         - ./prometheus.yml:/etc/prometheus/prometheus.yml  # Mount the Prometheus config file
       command:
         - '--config.file=/etc/prometheus/prometheus.yml'

     grafana:
       image: grafana/grafana
       container_name: grafana
       ports:
         - "3000:3000"
       volumes:
         - grafana-storage:/var/lib/grafana
       environment:
         - GF_SECURITY_ADMIN_PASSWORD=admin  # Set the default admin password

   volumes:
     grafana-storage:  # Define a volume for Grafana data persistence
   ```

---

### **Step 3.3: Create the `prometheus.yml` File**

1. **Where to Place the File**:
   - Create a file named `prometheus.yml` in the **root directory** of your project (the same folder as `docker-compose.yml`).

2. **Add the Following Content**:
   ```yaml
   global:
     scrape_interval: 15s  # How often to scrape metrics

   scrape_configs:
     - job_name: 'flask_app'
       static_configs:
         - targets: ['host.docker.internal:5000']  # Replace with your Flask app's host and port
   ```

   - **Explanation**:
     - `scrape_interval`: Defines how often Prometheus scrapes metrics from your Flask app.
     - `targets`: Replace `host.docker.internal:5000` with the host and port where your Flask app is running. If your app is running on `localhost:5000`, use `host.docker.internal:5000`.

---

### **Step 3.4: Start Prometheus and Grafana**

1. **Navigate to the Project Directory**:
   Open a terminal and navigate to the root directory of your project (where `docker-compose.yml` and `prometheus.yml` are located).

2. **Start the Services**:
   Run the following command to start Prometheus and Grafana:
   ```bash
   docker-compose up -d
   ```

   - This command will:
     - Download the required Docker images (if not already downloaded).
     - Start Prometheus and Grafana in detached mode (`-d`).

3. **Verify the Services**:
   - **Prometheus**: Open `http://localhost:9090` in your browser.
   - **Grafana**: Open `http://localhost:3000` in your browser.
     - Log in with the default credentials:
       - **Username**: `admin`
       - **Password**: `admin`

---

### **Step 3.5: Expose Flask Metrics**

To expose metrics from your Flask application, use the `prometheus-flask-exporter` library.

1. **Install the Library**:
   Run the following command to install the library:
   ```bash
   pip install prometheus-flask-exporter
   ```

2. **Update `app/__init__.py`**:
   Initialize the Prometheus metrics exporter in your Flask app:
   ```python
   from prometheus_flask_exporter import PrometheusMetrics

   def create_app():
       app = Flask(__name__)
       app.config.from_object(Config)

       db.init_app(app)
       jwt.init_app(app)

       # Initialize Prometheus metrics
       metrics = PrometheusMetrics(app)

       # Configure logging
       if not app.debug:
           if not os.path.exists('logs'):
               os.mkdir('logs')

           file_handler = RotatingFileHandler(
               'logs/microservice.log', maxBytes=10240, backupCount=10
           )
           file_handler.setFormatter(logging.Formatter(
               '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
           ))
           file_handler.setLevel(logging.INFO)
           app.logger.addHandler(file_handler)

           app.logger.setLevel(logging.INFO)
           app.logger.info('Microservice startup')

       with app.app_context():
           from . import routes
           app.register_blueprint(routes.bp)

           db.create_all()

       return app
   ```

3. **Access Metrics**:
   - Start your Flask application.
   - Metrics will be available at `http://localhost:5000/metrics`.

---

### **Step 3.6: Visualize Metrics in Grafana**

1. **Log in to Grafana**:
   - Open `http://localhost:3000` in your browser.
   - Log in with the username `admin` and password `admin`.

2. **Add Prometheus as a Data Source**:
   - Go to **Configuration > Data Sources**.
   - Click **Add data source**.
   - Select **Prometheus**.
   - Set the URL to `http://prometheus:9090` (if using Docker) or `http://localhost:9090` (if running locally).
   - Click **Save & Test**.

3. **Create a Dashboard**:
   - Go to **Create > Dashboard**.
   - Add a new panel.
   - Use Prometheus queries to visualize metrics. For example:
     - **Request Rate**: `rate(http_request_duration_seconds_count[1m])`
     - **Error Rate**: `rate(http_request_duration_seconds_count{status=~"5.."}[1m])`
     - **Response Time**: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[1m])) by (le)`

4. **Save the Dashboard**:
   - Give your dashboard a name and save it.

---

## **Directory Structure**
After completing the setup, your project directory should look like this:
```
your_project/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   └── ...
├── logs/
├── docker-compose.yml       # Added in the root directory
├── prometheus.yml           # Added in the root directory
└── ...
```

---

## **Summary**
In this section, we:
1. Added logging to track requests, errors, and important events.
2. Configured log levels and log file rotation.
3. Set up Prometheus and Grafana to monitor application performance.
4. Handled logging for Flask applications using the `@jwt_required` decorator.
5. Tested logging and monitoring.

Your microservice is now production-ready with proper logging and monitoring in place.

---

## **What’s Next?**
In **Part 6**, we’ll dive into **writing unit tests** for your Flask application. Unit testing is a critical step in ensuring your microservice is reliable, maintainable, and free of bugs. Here’s what you’ll learn:

- **Why Unit Testing Matters**: Understand the importance of unit tests in building robust applications.
- **Setting Up a Testing Environment**: Configure your Flask app for testing using tools like `pytest` and `unittest`.
- **Writing Unit Tests**: Create tests for your routes, models, and authentication logic.
- **Testing Edge Cases**: Learn how to test for unexpected inputs and error scenarios.
- **Running and Automating Tests**: Use tools to run tests automatically and integrate them into your development workflow.

By the end of **Part 6**, you’ll have a fully tested Flask microservice, giving you confidence in its functionality and stability. Stay tuned!

---

Let me know if you have further questions or need additional assistance! 🚀