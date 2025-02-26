from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .schemas import user_schema, ValidationError
from .models import User
from . import db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Welcome to the user management microservice"})

@bp.route('/register', methods=['POST'])
def register():
    try:
        # Validate and deserialize the input data
        data = user_schema.load(request.get_json())
    except ValidationError as err:
        current_app.logger.error(f"Validation: {err.messages}")
        return jsonify({"error": "Validation Error", "message": err.messages}), 400
    
    # Check if username or email already exists
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
        print(data)
    except ValidationError as err:
        current_app.logger.error(f"Validation error: {err.messages}")
        return jsonify({"error": "Validation Error", "message": err.messages}), 400

    username = data['username']
    password = data['password']

    # Log the received username and password
    current_app.logger.info(f"Login attempt for username: {username}")

    # Find the user
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        current_app.logger.info(f"User logged in: {user.username}")
        return jsonify(access_token=access_token), 200
    
    current_app.logger.warning(f"Invalid login attempt for username: {username}")
    return jsonify({"error": "Invalid credentials"}), 401


@bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    users = User.query.all()
    return jsonify([{
        "id": user.id,
        "username": user.username,
        "email": user.email
    } for user in users])

@bp.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })

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

@bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    if not user:
        current_app.logger.warning(f"Unauthorized access attempt by user ID: {current_user_id}")
        return jsonify({"error": "User not found"}), 404

    current_app.logger.info(f"Authorized access by user: {user.username}")
    return jsonify({"message": f"Hello, {user.username}!"}), 200
