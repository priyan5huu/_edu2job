import datetime
from datetime import timezone
import bcrypt

try:
    from .extensions import db
except (ImportError, ValueError):
    from extensions import db

def utcnow():
    return datetime.datetime.now(timezone.utc)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow)

    # profile fields (optional)
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))
    headline = db.Column(db.String(200))
    summary = db.Column(db.Text)
    security_question = db.Column(db.String(200))
    security_answer = db.Column(db.String(200))
    profile_picture = db.Column(db.String(255)) # URL or path to image

    def __init__(self, username, email, password, security_question=None, security_answer=None):
        self.username = username
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.security_question = security_question
        if security_answer:
            self.security_answer = bcrypt.hashpw(security_answer.lower().strip().encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        else:
            self.security_answer = None

    def check_password(self, password):
        try:
            return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
        except Exception:
            return False

    def check_security_answer(self, answer):
        try:
            if not self.security_answer or not answer:
                return False
            return bcrypt.checkpw(answer.lower().strip().encode('utf-8'), self.security_answer.encode('utf-8'))
        except Exception:
            return False

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    def check_password(self, password):
        try:
            return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
        except Exception:
            return False

class PasswordResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(128), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)

    def is_valid(self):
        now = utcnow()
        if self.expires_at.tzinfo is not None:
            expires_naive = self.expires_at.replace(tzinfo=None)
        else:
            expires_naive = self.expires_at
        return (not self.used) and (now < expires_naive)

class PredictionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    predicted_role = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    salary_range = db.Column(db.String(50))
    degree = db.Column(db.String(100))
    major = db.Column(db.String(100))
    specialization = db.Column(db.String(100))
    cgpa = db.Column(db.Float)
    years_of_experience = db.Column(db.Integer)
    skills = db.Column(db.Text)
    certifications = db.Column(db.Text)
    preferred_industry = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=utcnow)
    
    def to_dict(self):
        now = utcnow()
        created_at = self.created_at if self.created_at.tzinfo else self.created_at.replace(tzinfo=timezone.utc)
        delta = now - created_at
        
        if delta.days > 365:
            years = delta.days // 365
            time_ago = f"{years} year{'s' if years > 1 else ''} ago"
        elif delta.days > 30:
            months = delta.days // 30
            time_ago = f"{months} month{'s' if months > 1 else ''} ago"
        elif delta.days > 0:
            time_ago = f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
        elif delta.seconds > 3600:
            hours = delta.seconds // 3600
            time_ago = f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif delta.seconds > 60:
            minutes = delta.seconds // 60
            time_ago = f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            time_ago = "Just now"
        
        search_title = f"{self.degree} in {self.major}"
        if self.specialization:
            search_title += f" - {self.specialization}"
        
        return {
            'id': self.id,
            'predicted_role': self.predicted_role,
            'confidence': round(self.confidence, 1),
            'salary_range': self.salary_range,
            'search_title': search_title,
            'time_ago': time_ago,
            'created_at': self.created_at.isoformat(),
            'input_data': {
                'degree': self.degree,
                'major': self.major,
                'specialization': self.specialization,
                'cgpa': self.cgpa,
                'years_of_experience': self.years_of_experience,
                'skills': self.skills,
                'certifications': self.certifications,
                'preferred_industry': self.preferred_industry
            }
        }
