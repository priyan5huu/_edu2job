import os
import sys
import logging
import secrets
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, send_from_directory
from dotenv import load_dotenv
import joblib

# Import extensions and models
try:
    from .extensions import db, cors, limiter
    from .models import Admin
    from .routes.auth import auth_bp
    from .routes.profile import profile_bp
    from .routes.prediction import prediction_bp, prediction_bp as pred_module
    from .routes.admin import admin_bp
except (ImportError, ValueError):
    from extensions import db, cors, limiter
    from models import Admin
    from routes.auth import auth_bp
    from routes.profile import profile_bp
    from routes.prediction import prediction_bp, prediction_bp as pred_module
    from routes.admin import admin_bp

load_dotenv()

def create_app():
    app = Flask(__name__, static_folder='../frontend')
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(32))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ACCESS_TOKEN_EXPIRES'] = int(os.getenv('ACCESS_TOKEN_EXPIRES_SECONDS', 604800))
    app.config['REFRESH_TOKEN_EXPIRES'] = int(os.getenv('REFRESH_TOKEN_EXPIRES_SECONDS', 1209600))
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../frontend/uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    limiter.init_app(app)

    # Logging
    os.makedirs('logs', exist_ok=True)
    file_handler = RotatingFileHandler('logs/edu2job.log', maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(admin_bp)

    # Load ML models
    load_ml_models(app)

    # Database setup
    with app.app_context():
        db.create_all()
        if not Admin.query.filter_by(username='admin').first():
            db.session.add(Admin('admin', 'admin123'))
            db.session.commit()

    # Base routes
    @app.route('/')
    def index():
        return send_from_directory('../frontend', 'login.html')

    @app.route('/<path:filename>')
    def serve_static(filename):
        return send_from_directory('../frontend', filename)

    @app.route('/health')
    def health():
        return jsonify({"status": "healthy", "ml_loaded": pred_module.ML_MODEL is not None}), 200

    return app

def load_ml_models(app):
    try:
        model_dir = os.path.join(os.path.dirname(__file__), 'models')
        model_path = os.path.join(model_dir, 'best_model.pkl')
        preprocessor_path = os.path.join(model_dir, 'preprocessor.pkl')
        
        if os.path.exists(model_path) and os.path.exists(preprocessor_path):
            # Add ml directory to path for custom preprocessor
            ml_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml')
            if os.path.exists(ml_dir):
                sys.path.insert(0, ml_dir)
                from preprocess import Edu2JobPreprocessor
                import __main__
                __main__.Edu2JobPreprocessor = Edu2JobPreprocessor
            
            pred_module.ML_MODEL = joblib.load(model_path)
            pred_module.ML_PREPROCESSOR = joblib.load(preprocessor_path)
            app.logger.info("✅ ML models loaded successfully")
        else:
            app.logger.warning("⚠️ ML model files not found in backend/models/")
    except Exception as e:
        app.logger.error(f"❌ Error loading models: {e}")

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000)), debug=True)
