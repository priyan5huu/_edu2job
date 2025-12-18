import datetime
import time
from flask import Blueprint, request, jsonify, make_response, current_app

try:
    from ..extensions import db, limiter
    from ..models import User, PasswordResetToken
    from ..utils import (
        sanitize_input, validate_email, validate_password_strength, 
        generate_token, generate_reset_token, utcnow
    )
except (ImportError, ValueError):
    from extensions import db, limiter
    from models import User, PasswordResetToken
    from utils import (
        sanitize_input, validate_email, validate_password_strength, 
        generate_token, generate_reset_token, utcnow
    )

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@limiter.limit("50 per minute")
def register():
    data = request.get_json() or {}
    username = sanitize_input(data.get('username', ''))
    email = (data.get('email') or '').strip().lower()
    password = data.get('password', '')
    security_question = sanitize_input(data.get('security_question', ''))
    security_answer = sanitize_input(data.get('security_answer', ''))

    if not username or not email or not password or not security_question or not security_answer:
        return jsonify({"message": "All fields required"}), 400
    if not validate_email(email):
        return jsonify({"message": "Invalid email"}), 400
    ok, msg = validate_password_strength(password)
    if not ok:
        return jsonify({"message": msg}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 409
    user = User(username, email, password, security_question, security_answer)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered", "username": user.username, "email": user.email}), 201

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("50 per minute")
def login():
    data = request.get_json() or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token_expires = current_app.config['ACCESS_TOKEN_EXPIRES']
    refresh_token_expires = current_app.config['REFRESH_TOKEN_EXPIRES']

    access_payload = {"user_id": user.id, "type": "access"}
    refresh_payload = {"user_id": user.id, "type": "refresh"}

    access_token = generate_token(access_payload, access_token_expires)
    refresh_token = generate_token(refresh_payload, refresh_token_expires)

    current_app.logger.info(f"Login successful for user {user.id}")

    resp = make_response(jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {"id": user.id, "username": user.username, "email": user.email}
    }))
    resp.set_cookie('access_token', access_token, httponly=True, samesite='Lax', max_age=access_token_expires)
    resp.set_cookie('refresh_token', refresh_token, httponly=True, samesite='Lax', max_age=refresh_token_expires)
    return resp, 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    resp = make_response(jsonify({"success": True, "message": "Logged out successfully"}))
    resp.set_cookie('access_token', '', expires=0, httponly=True, samesite='Lax')
    resp.set_cookie('refresh_token', '', expires=0, httponly=True, samesite='Lax')
    return resp, 200

@auth_bp.route('/forgot-password', methods=['POST'])
@limiter.limit("50 per minute")
def forgot_password():
    data = request.get_json() or {}
    email = (data.get('email') or '').strip().lower()
    if not email or not validate_email(email):
        return jsonify({"success": False, "message": "Invalid email format"}), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": False, "message": "If this email is registered, you will receive password reset instructions"}), 404
    if not user.security_question:
        return jsonify({"success": False, "message": "Password reset not available for this account."}), 400
    return jsonify({
        "success": True,
        "message": "Please answer your security question",
        "security_question": user.security_question,
        "email": email
    }), 200

@auth_bp.route('/verify-security-answer', methods=['POST'])
@limiter.limit("50 per minute")
def verify_security_answer():
    data = request.get_json() or {}
    email = (data.get('email') or '').strip().lower()
    answer = sanitize_input(data.get('answer', ''))
    if not email or not answer:
        return jsonify({"success": False, "message": "Email and answer are required"}), 400
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_security_answer(answer):
        return jsonify({"success": False, "message": "Invalid answer"}), 401
    token = generate_reset_token(32)
    expires_at = utcnow() + datetime.timedelta(minutes=15)
    PasswordResetToken.query.filter_by(user_id=user.id, used=False).update({'used': True})
    reset_token_entry = PasswordResetToken(user_id=user.id, token=token, expires_at=expires_at)
    db.session.add(reset_token_entry)
    db.session.commit()
    return jsonify({"success": True, "message": "Answer verified", "reset_token": token}), 200

@auth_bp.route('/reset-password', methods=['POST'])
@limiter.limit("50 per minute")
def reset_password():
    data = request.get_json() or {}
    token = data.get('reset_token', '').strip()
    new_password = data.get('new_password', '')
    confirm_password = data.get('confirm_password', '')
    if not token or not new_password or not confirm_password:
        return jsonify({"success": False, "message": "All fields are required"}), 400
    if new_password != confirm_password:
        return jsonify({"success": False, "message": "Passwords do not match"}), 400
    ok, msg = validate_password_strength(new_password)
    if not ok:
        return jsonify({"success": False, "message": msg}), 400
    reset = PasswordResetToken.query.filter_by(token=token, used=False).first()
    if not reset or not reset.is_valid():
        return jsonify({"success": False, "message": "Invalid or expired reset token"}), 400
    user = db.session.get(User, reset.user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    import bcrypt
    user.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    reset.used = True
    db.session.commit()
    return jsonify({"success": True, "message": "Password reset successful"}), 200
