import os
import time
import base64
from flask import Blueprint, request, jsonify, current_app

try:
    from ..extensions import db
    from ..utils import login_required, sanitize_input
except (ImportError, ValueError):
    from extensions import db
    from utils import login_required, sanitize_input

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/api/profile', methods=['GET'])
@login_required
def get_profile(user):
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "location": user.location,
        "headline": user.headline,
        "profile_picture": user.profile_picture,
        "summary": user.summary
    }), 200

@profile_bp.route('/api/profile', methods=['PUT'])
@login_required
def update_profile(user):
    data = request.get_json() or {}
    user.phone = sanitize_input(data.get('phone', user.phone))
    user.location = sanitize_input(data.get('location', user.location))
    user.headline = sanitize_input(data.get('headline', user.headline), max_length=200)
    user.summary = sanitize_input(data.get('summary', user.summary), max_length=2000)
    
    if 'profile_picture' in data and data['profile_picture']:
        try:
            if "," in data['profile_picture']:
                header, encoded = data['profile_picture'].split(",", 1)
                ext = "png"
                if "jpeg" in header or "jpg" in header: ext = "jpg"
                elif "gif" in header: ext = "gif"
                
                filename = f"user_{user.id}_{int(time.time())}.{ext}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                
                with open(file_path, "wb") as f:
                    f.write(base64.b64decode(encoded))
                
                user.profile_picture = filename
        except Exception as e:
            current_app.logger.error(f"Image upload failed: {e}")

    db.session.commit()
    return jsonify({"message": "Profile updated", "profile_picture": user.profile_picture}), 200
