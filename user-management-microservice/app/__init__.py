import os
import logging
from logging.handlers import RotatingFileHandler
from prometheus_flask_exporter import PrometheusMetrics
from flask import Flask, jsonify, request
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

    # Initialize Prometheus metrics
    metrics = PrometheusMetrics(app)  # Enable default metrics

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

