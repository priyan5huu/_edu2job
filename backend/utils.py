import re
import time
import jwt
import secrets
import string
from functools import wraps
from flask import request, jsonify, current_app

try:
    from .extensions import db
    from .models import User, Admin
except (ImportError, ValueError):
    from extensions import db
    from models import User, Admin

def sanitize_input(text, max_length=1000):
    if text is None:
        return None
    text = re.sub(r'<[^>]*>', '', str(text))
    return text.strip()[:max_length]

def validate_email(email):
    if not email:
        return False
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def validate_password_strength(password):
    if not password or len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain a letter"
    if not re.search(r'\d', password):
        return False, "Password must contain a number"
    return True, "OK"

def generate_token(payload, expire_seconds):
    now = int(time.time())
    payload_copy = payload.copy()
    payload_copy['exp'] = now + int(expire_seconds)
    return jwt.encode(payload_copy, current_app.config['SECRET_KEY'], algorithm='HS256')

def decode_token(token):
    return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])

def generate_reset_token(length=64):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def token_from_request():
    token = request.cookies.get('access_token')
    if not token and 'Authorization' in request.headers:
        parts = request.headers.get('Authorization').split()
        if len(parts) == 2 and parts[0] == 'Bearer':
            token = parts[1]
    return token

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = token_from_request()
        if not token:
            return jsonify({"message": "Token missing"}), 401
        try:
            decoded = decode_token(token)
            user = db.session.get(User, decoded.get('user_id'))
            if not user:
                return jsonify({"message": "User not found"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
        except Exception as e:
            current_app.logger.error(f"Token decode error: {e}")
            return jsonify({"message": "Token error"}), 401
        return f(user, *args, **kwargs)
    return wrapper

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = token_from_request()
        if not token:
            return jsonify({"message": "Admin token missing"}), 401
        try:
            decoded = decode_token(token)
            if decoded.get('role') != 'admin':
                return jsonify({"message": "Admin role required"}), 403
            admin = Admin.query.get(decoded.get('admin_id'))
            if not admin:
                return jsonify({"message": "Admin not found"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Admin token expired"}), 401
        except Exception as e:
            current_app.logger.error(f"Admin token error: {e}")
            return jsonify({"message": "Admin token invalid"}), 401
        return f(admin, *args, **kwargs)
    return wrapper
