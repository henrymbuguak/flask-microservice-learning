from flask import Flask, jsonify
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

    @app.errorhandler(404)
    def not_found(error):
        return  jsonify({"error": "Not Found", "message": "The requested resource was not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal Server Error", "message": "Something went wrong on the server"}), 500

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

        db.create_all()

    return app

