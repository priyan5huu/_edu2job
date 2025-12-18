from flask import Blueprint, request, jsonify, current_app

try:
    from ..extensions import db
    from ..models import User, Admin
    from ..utils import admin_required, generate_token
except (ImportError, ValueError):
    from extensions import db
    from models import User, Admin
    from utils import admin_required, generate_token

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')
    admin = Admin.query.filter_by(username=username).first()
    if not admin or not admin.check_password(password):
        return jsonify({"message": "Invalid admin credentials"}), 401
    payload = {"admin_id": admin.id, "role": "admin"}
    token = generate_token(payload, current_app.config['ACCESS_TOKEN_EXPIRES'] * 4)
    return jsonify({"token": token, "message": "Admin login successful"}), 200

@admin_bp.route('/api/users', methods=['GET'])
@admin_required
def admin_get_users(admin):
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username, "email": u.email} for u in users]), 200

@admin_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
@admin_required
def admin_delete_user(admin, user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200
