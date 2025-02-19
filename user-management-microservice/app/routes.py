from flask import Blueprint, jsonify

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Welcome to the user management microservice"})
