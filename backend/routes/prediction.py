import os
import pandas as pd
import numpy as np
from flask import Blueprint, request, jsonify, current_app

try:
    from ..extensions import db
    from ..models import PredictionHistory
    from ..utils import login_required
except (ImportError, ValueError):
    from extensions import db
    from models import PredictionHistory
    from utils import login_required

prediction_bp = Blueprint('prediction', __name__)

# These will be set by the app
ML_MODEL = None
ML_PREPROCESSOR = None

def estimate_salary(job_role, years_of_experience, cgpa):
    salary_ranges = {
        'Software Engineer': (6, 18), 'Data Scientist': (8, 25), 'Full Stack Developer': (6, 20),
        'Machine Learning Engineer': (10, 30), 'DevOps Engineer': (7, 22), 'Product Manager': (12, 35),
        'Business Analyst': (5, 15), 'Data Analyst': (5, 15), 'Web Developer': (4, 15),
        'Mobile App Developer': (6, 18), 'Cloud Architect': (15, 40), 'Cybersecurity Analyst': (8, 25),
        'AI Engineer': (12, 35), 'Backend Developer': (6, 20), 'Frontend Developer': (5, 18),
        'UI/UX Designer': (5, 16), 'QA Engineer': (4, 14), 'System Administrator': (5, 15),
        'Database Administrator': (7, 20), 'Network Engineer': (6, 18),
    }
    base_min, base_max = salary_ranges.get(job_role, (5, 15))
    exp_multiplier = 1 + (years_of_experience * 0.15) if years_of_experience <= 2 else (1.3 + (years_of_experience - 2) * 0.12 if years_of_experience <= 5 else 1.66 + (years_of_experience - 5) * 0.08)
    cgpa_multiplier = 1.15 if cgpa >= 8.5 else (1.08 if cgpa >= 7.5 else (1.00 if cgpa >= 6.5 else 0.95))
    adjusted_min = max(int(base_min * exp_multiplier * cgpa_multiplier), 3)
    adjusted_max = max(int(base_max * exp_multiplier * cgpa_multiplier), adjusted_min + 3)
    return f"₹{adjusted_min}-{adjusted_max} LPA"

def generate_job_predictions_fallback(degree, major, specialization, cgpa, years_of_experience, skills, certifications, preferred_industry):
    job_roles = {
        "Software Engineer": {"majors": ["computer science", "software engineering"], "skills": ["python", "java", "javascript"], "min_cgpa": 6.5, "salary": "₹6-18 LPA"},
        "Data Scientist": {"majors": ["data science", "statistics"], "skills": ["python", "machine learning", "sql"], "min_cgpa": 7.0, "salary": "₹8-25 LPA"},
        "Full Stack Developer": {"majors": ["computer science"], "skills": ["javascript", "react", "node"], "min_cgpa": 6.0, "salary": "₹6-20 LPA"},
        "Business Analyst": {"majors": ["business", "management"], "skills": ["excel", "sql", "tableau"], "min_cgpa": 6.5, "salary": "₹5-15 LPA"},
        "Data Analyst": {"majors": ["statistics", "data science"], "skills": ["sql", "excel", "python"], "min_cgpa": 6.5, "salary": "₹5-15 LPA"}
    }
    predictions = []
    skills_lower = [s.strip().lower() for s in skills.split(',')]
    major_lower = major.lower()
    for role, reqs in job_roles.items():
        score = (40 if any(m in major_lower for m in reqs["majors"]) else 0) + int(sum(1 for s in reqs["skills"] if any(s in us for us in skills_lower)) / len(reqs["skills"]) * 40) + (10 if cgpa >= reqs["min_cgpa"] else 0) + (10 if years_of_experience >= 2 else 0)
        if score > 20: predictions.append({"job_role": role, "confidence": round(min(100, score), 1), "salary": reqs["salary"], "details": {"salary_range": reqs["salary"]}})
    predictions.sort(key=lambda x: x["confidence"], reverse=True)
    return predictions[:5] if predictions else [{"job_role": "General Analyst", "confidence": 50.0, "salary": "₹4-12 LPA", "details": {"salary_range": "₹4-12 LPA"}}]

def generate_roadmap(job_role):
    roadmaps = {
        "Software Engineer": [{"step": i+1, "title": t, "desc": d} for i, (t, d) in enumerate([("Programming Basics", "Python/Java"), ("Web Fundamentals", "HTML/CSS/JS"), ("Version Control", "Git"), ("Databases", "SQL/NoSQL"), ("Frameworks", "React/Django"), ("System Design", "Scalability")])],
        "Data Scientist": [{"step": i+1, "title": t, "desc": d} for i, (t, d) in enumerate([("Math & Stats", "Linear Algebra"), ("Python for Data", "Pandas/NumPy"), ("Machine Learning", "Scikit-Learn"), ("Deep Learning", "TensorFlow"), ("Big Data", "Spark/SQL"), ("Deployment", "Docker/MLOps")])],
    }
    return roadmaps.get(job_role, [{"step": i+1, "title": f"Step {i+1}", "desc": f"Learn {job_role} basics"} for i in range(6)])

@prediction_bp.route('/api/predict-job', methods=['POST'])
@login_required
def predict_job(user):
    try:
        data = request.get_json() or {}
        degree, major, specialization = data.get('degree', '').strip(), data.get('major', '').strip(), data.get('specialization', '').strip()
        cgpa, years_of_experience = data.get('cgpa'), data.get('years_of_experience')
        skills, certifications, preferred_industry = data.get('skills', '').strip(), data.get('certifications', '').strip(), data.get('preferred_industry', '').strip()

        if not all([degree, major, specialization, preferred_industry, skills]):
            return jsonify({"success": False, "message": "Required fields missing"}), 400

        try:
            cgpa, years_of_experience = float(cgpa), float(years_of_experience)
        except:
            return jsonify({"success": False, "message": "Invalid numeric format"}), 400

        if ML_MODEL and ML_PREPROCESSOR:
            try:
                input_df = pd.DataFrame([{'Degree': degree, 'Major': major, 'Specialization': specialization, 'CGPA': cgpa, 'Skills': skills, 'Certification': certifications or 'None', 'Years of Experience': years_of_experience, 'Preferred Industry': preferred_industry}])
                X_transformed = ML_PREPROCESSOR.transform(input_df, is_training=False)
                probs = ML_MODEL.predict_proba(X_transformed)[0]
                top_indices = np.argsort(probs)[-5:][::-1]
                encoder = ML_PREPROCESSOR.label_encoders.get('Job Role')
                preds = [{"job_role": encoder.inverse_transform([i])[0], "confidence": round(probs[i]*100, 1), "salary": estimate_salary(encoder.inverse_transform([i])[0], years_of_experience, cgpa)} for i in top_indices if probs[i]*100 > 1]
            except Exception as e:
                current_app.logger.error(f"ML error: {e}")
                preds = generate_job_predictions_fallback(degree, major, specialization, cgpa, years_of_experience, skills, certifications, preferred_industry)
        else:
            preds = generate_job_predictions_fallback(degree, major, specialization, cgpa, years_of_experience, skills, certifications, preferred_industry)

        top_pred = preds[0]
        history_entry = PredictionHistory(user_id=user.id, predicted_role=top_pred['job_role'], confidence=top_pred['confidence'], salary_range=top_pred['salary'], degree=degree, major=major, specialization=specialization, cgpa=cgpa, years_of_experience=years_of_experience, skills=skills, certifications=certifications, preferred_industry=preferred_industry)
        db.session.add(history_entry)
        db.session.commit()

        return jsonify({"success": True, "predicted_role": top_pred['job_role'], "match_percentage": top_pred['confidence'], "salary_range": top_pred['salary'], "description": f"As a {top_pred['job_role']}, you will work in {preferred_industry}.", "roadmap": generate_roadmap(top_pred['job_role']), "top_alternative_roles": [{"role": p['job_role'], "match": p['confidence']} for p in preds[1:4]]}), 200
    except Exception as e:
        current_app.logger.error(f"Predict error: {e}")
        db.session.rollback()
        return jsonify({"success": False, "message": "Internal error"}), 500

@prediction_bp.route('/api/prediction-history', methods=['GET'])
@login_required
def get_prediction_history(user):
    predictions = PredictionHistory.query.filter_by(user_id=user.id).order_by(PredictionHistory.created_at.desc()).limit(50).all()
    return jsonify({"history": [p.to_dict() for p in predictions]}), 200

@prediction_bp.route('/api/get-options', methods=['GET'])
def get_options():
    try:
        csv_path = os.path.join(current_app.root_path, 'models/JobRole.csv')
        if not os.path.exists(csv_path):
            csv_path = os.path.join(os.path.dirname(current_app.root_path), 'JobRole.csv')
        
        df = pd.read_csv(csv_path)
        all_skills = set(df['Skills'].dropna().str.split(',').explode().str.strip())
        all_skills.update(["Python", "Java", "JavaScript", "React", "Node.js", "SQL", "AWS", "Docker", "Git"])
        
        return jsonify({
            'Degree': sorted(df['Degree'].unique().tolist()),
            'Major': sorted(df['Major'].unique().tolist()),
            'Specialization': sorted(df['Specialization'].unique().tolist()) if 'Specialization' in df.columns else [],
            'Preferred Industry': sorted(df['Preferred Industry'].unique().tolist()),
            'Skills': sorted(list(all_skills)),
            'Certifications': sorted(list(set(df['Certification'].dropna().str.split(',').explode().str.strip()) | {"AWS Certified", "PMP", "Google Analytics"}))
        }), 200
    except Exception as e:
        current_app.logger.error(f"Options error: {e}")
        return jsonify({"message": "Error loading options"}), 500
