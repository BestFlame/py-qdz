from flask import Blueprint, request, jsonify
from ..service.user_service import register_user, authenticate_user

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    result, status = register_user(email, password)
    return jsonify(result), status

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user, status = authenticate_user(email, password)
    return jsonify({'user': user, 'status': 'success' if status == 200 else 'failed'}), status