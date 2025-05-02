from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user, logout_user
from service.user_service import register_user, authenticate_user

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    result, status = register_user(email, password)
    return jsonify(result), status

@user_bp.route('/profile')
@login_required
def profile():
    return render_template('person/user_profile.html')

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

