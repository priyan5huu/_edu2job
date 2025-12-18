# 🎓 Edu2Job - AI-Powered Career Prediction & Resume Builder Platform

> **Transform Your Education into Your Dream Career**

A comprehensive full-stack web application that uses Machine Learning to predict optimal career paths based on educational background, skills, and experience. Features an advanced resume builder with ATS optimization, cover letter generation, and job-specific customization.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [ML Model Details](#ml-model-details)
- [Frontend Features](#frontend-features)
- [Security Features](#security-features)
- [Deployment](#deployment)
- [Future Roadmap](#future-roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**Edu2Job** is an intelligent career guidance platform that helps students and professionals make data-driven career decisions. By analyzing your educational background, skills, certifications, and experience, our ML model predicts the best-fit job roles and provides comprehensive career insights.

### Problem Statement
- Students struggle to identify optimal career paths after graduation
- Misalignment between education and job market demands
- Lack of personalized career guidance
- Time-consuming resume creation and optimization
- Difficulty tailoring applications for specific jobs

### Solution
- **AI-Powered Predictions:** Machine learning model trained on 2,200+ career profiles
- **Comprehensive Career Insights:** Salary ranges, growth rates, skill gaps, learning roadmap
- **Smart Resume Builder:** ATS-optimized resumes with 3 professional templates
- **Cover Letter Generator:** AI-powered, personalized cover letters
- **Job-Specific Customization:** Tailor your resume for specific job postings
- **Profile Management:** Store and manage your professional profile

---

## ✨ Key Features

### 🤖 Career Prediction Engine
- **ML-Powered Analysis:** Logistic Regression model with 92%+ accuracy
- **15 Job Role Categories:** From Software Engineer to Marketing Manager
- **Confidence Scores:** Match percentage for each predicted role
- **Skill Gap Analysis:** Identifies missing skills for target roles
- **Alternative Career Paths:** Top 3 alternative role suggestions
- **Salary Predictions:** Expected salary ranges for each role
- **Growth Rate Insights:** Career progression timelines
- **Learning Roadmap:** Step-by-step career development plan
- **Certification Recommendations:** Industry-relevant certifications
- **Market Positioning:** Compare your profile vs market average

### 📄 Advanced Resume Builder
- **3 Professional Templates:** Modern, Classic, Creative designs
- **ATS Score Analyzer:** Check resume compatibility with Applicant Tracking Systems
- **Real-time Preview:** Instant resume generation and preview
- **One-Click Download:** Print-optimized PDF export
- **Resume Version Manager:** Save and manage multiple resume versions
- **Keyword Optimizer:** Optimize for specific job titles
- **Projects Showcase:** Display up to 10 professional projects
- **Skills & Certifications:** Tag-based input with autocomplete
- **Social Links Integration:** LinkedIn, GitHub, Portfolio links
- **Multi-language Support:** Add language proficiency levels

### 📝 Cover Letter Generator ⭐ **NEW**
- **AI-Powered Generation:** Personalized cover letters in seconds
- **4 Tone Options:** Professional, Enthusiastic, Confident, Humble
- **Company-Specific:** Tailored for each job application
- **Auto-Populated:** Uses your profile data automatically
- **Professional Formatting:** Business letter structure
- **Achievements Integration:** Highlights your key accomplishments

### 🎯 Job-Specific Customizer ⭐ **NEW**
- **Job Description Analysis:** Paste any job posting
- **Match Score Calculation:** 0-100% compatibility rating
- **Missing Skills Detection:** Identifies gaps in your profile
- **Tailored Recommendations:** Specific improvement suggestions
- **Keyword Extraction:** Auto-detects job requirements
- **Resume Optimization:** Guidance on what to emphasize

### 💼 LinkedIn Integration ⭐ **NEW**
- **Quick Import:** Auto-fill profile from LinkedIn URL
- **Time-Saving:** Eliminates manual data entry
- **Data Accuracy:** Reduces typing errors

### 📧 Email Resume Feature ⭐ **NEW**
- **Direct Sending:** Email resume to recruiters
- **Professional Template:** Pre-formatted email body
- **Quick Application:** Apply without downloading

### 👤 Profile Management
- **Comprehensive Profile:** Education, experience, skills, certifications
- **Social Integration:** LinkedIn, GitHub, Portfolio links
- **Project Portfolio:** Showcase up to 10 projects
- **Achievements Section:** Awards and accomplishments
- **Languages:** Proficiency levels (Beginner to Native)
- **Profile Completion:** Real-time completion percentage
- **Auto-Save:** Data persisted in localStorage
- **Privacy:** User-specific data isolation

### 📊 Prediction History
- **Historical Tracking:** All past predictions saved
- **Search & Filter:** Find specific predictions quickly
- **Delete Management:** Remove old predictions
- **Detailed View:** Complete prediction breakdown
- **Trend Analysis:** Track career exploration journey

---

## 🛠️ Tech Stack

### Frontend
- **HTML5/CSS3:** Semantic markup and modern styling
- **Vanilla JavaScript:** No framework dependencies, lightweight
- **Chart.js:** Interactive radar and bar charts
- **Google Fonts:** Inter & Space Grotesk typography
- **Responsive Design:** Mobile-first approach
- **CSS Variables:** Dynamic theming
- **Local Storage:** Client-side data persistence

### Backend
- **Python 3.9+:** Modern Python features
- **Flask 3.0.0:** Lightweight web framework
- **Flask-SQLAlchemy:** ORM for database operations
- **Flask-CORS:** Cross-origin resource sharing
- **Flask-Limiter:** API rate limiting
- **SQLite:** Development database
- **MySQL:** Production database (optional)

### Machine Learning
- **scikit-learn 1.3.2:** ML model training and inference
- **pandas 2.1.4:** Data manipulation
- **numpy 1.26.2:** Numerical computations
- **joblib 1.3.2:** Model serialization
- **TF-IDF Vectorization:** Text feature extraction
- **Logistic Regression:** Classification model
- **Feature Engineering:** 181 features from 6 input fields

### Security
- **bcrypt 4.1.1:** Password hashing
- **PyJWT 2.8.0:** JWT token generation
- **python-dotenv 1.0.0:** Environment variable management
- **cryptography 41.0.7:** Secure data encryption
- **CORS Protection:** Domain whitelisting
- **Rate Limiting:** Prevent API abuse
- **Input Validation:** XSS and injection prevention

---

## 📁 Project Structure

```
edu2job/
├── backend/
│   ├── app.py                    # Application factory and entry point
│   ├── extensions.py             # Flask extensions (DB, CORS, Limiter)
│   ├── models.py                 # Database models
│   ├── utils.py                  # Backend helper functions & decorators
│   ├── routes/                   # Flask Blueprints
│   │   ├── auth.py               # Auth routes
│   │   ├── profile.py            # Profile routes
│   │   ├── prediction.py         # ML prediction routes
│   │   └── admin.py              # Admin routes
│   ├── models/                   # ML assets and datasets
│   │   ├── best_model.pkl        # Trained ML model
│   │   ├── preprocessor.pkl      # Preprocessing pipeline
│   │   ├── label_encoders.pkl    # Encoders
│   │   ├── scaler.pkl            # Scaler
│   │   ├── model_info.json       # Model metadata
│   │   └── JobRole.csv           # Training dataset
│   └── uploads/                  # User profile pictures
│
├── frontend/
│   ├── index.html                # Landing page
│   ├── login.html                # Login page
│   ├── register.html             # Registration page
│   ├── dashboard.html            # Main dashboard
│   ├── css/
│   │   └── global.css            # Shared design system & components
│   └── js/
│       ├── config.js             # Centralized frontend config
│       └── utils.js              # Shared frontend utilities (Toast, Auth)
│
├── ml/
│   └── preprocess.py             # ML preprocessing logic (shared with backend)
│
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables
├── .gitignore                    # Git ignore rules
├── start.sh                      # Server startup script
├── stop.sh                       # Server stop script
└── README.md                     # This file
```

### Key Files Explained

#### `backend/` (Refactored)
- **Modular Architecture:** Split into Blueprints (auth, profile, prediction, admin) for better maintainability.
- **Extensions:** Centralized initialization of DB, CORS, and Rate Limiter.
- **Models:** Unified database schema definitions.
- **ML Assets:** All model-related files consolidated in `backend/models/`.

#### `frontend/` (Modularized)
- **Shared Utilities:** `js/utils.js` provides unified Toast notifications and Auth checks.
- **Centralized Config:** `js/config.js` manages API URLs and app settings.
- **Global CSS:** `css/global.css` implements the design system across all pages.
- **Dashboard:** Cleaned up and refactored to use shared modules.

#### `ml/preprocess.py`
- **Feature Engineering:** Converts raw input to 181 features
- **TF-IDF Vectorization:** Text feature extraction for skills
- **Label Encoding:** Categorical feature transformation
- **Scaling:** StandardScaler for numerical features
- **Pipeline Integration:** Seamless model inference

#### `best_model.pkl` (Trained Model)
- **Algorithm:** Logistic Regression (Tuned)
- **Training Date:** November 26, 2025
- **Training Samples:** 1,800 profiles
- **Test Samples:** 402 profiles
- **Features:** 181 engineered features
- **Classes:** 15 job role categories
- **Accuracy:** 92%+ on test set
- **F1 Score:** 0.89 (weighted average)

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git (optional)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/edu2job.git
cd edu2job
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production

# Database Configuration
DATABASE_URL=sqlite:///instance/database.db

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-here-change-in-production
JWT_EXPIRATION_HOURS=24

# CORS Configuration
FRONTEND_URL=http://127.0.0.1:5500

# API Rate Limiting
RATELIMIT_STORAGE_URL=memory://
```

**Important:** Change `SECRET_KEY` and `JWT_SECRET_KEY` to random, secure strings in production!

### Step 5: Initialize Database
```bash
# The database will be automatically created on first run
# Or manually initialize:
python -c "from backend.app import db; db.create_all()"
```

### Step 6: Start the Server
```bash
# Using the startup script (recommended)
./start.sh

# Or manually:
python backend/app.py

# The server will start on http://localhost:8000
```

### Step 7: Open Frontend
```bash
# Option 1: Use Live Server (VS Code extension)
# Right-click on frontend/index.html → Open with Live Server

# Option 2: Use Python HTTP server
cd frontend
python -m http.server 5500

# Option 3: Open directly in browser
# Open frontend/index.html in your browser
```

### Step 8: Test the Application
1. Navigate to `http://localhost:5500/index.html`
2. Click "Get Started" or "Sign Up"
3. Register a new account
4. Login with your credentials
5. Complete your profile
6. Generate a career prediction
7. Build your resume

---

## 📖 Usage Guide

### 1. Getting Started

#### Registration
1. Go to the landing page (`index.html`)
2. Click "Get Started" or "Sign Up"
3. Fill in:
   - Username (3-50 characters, alphanumeric)
   - Email (valid email format)
   - Password (minimum 6 characters)
4. Click "Create Account"
5. You'll be redirected to the dashboard

#### Login
1. Click "Login" on the landing page
2. Enter your credentials
3. Click "Sign In"
4. Access the dashboard

### 2. Building Your Profile

#### Personal Information
- **Full Name:** Your complete name
- **Email:** Contact email (pre-filled from registration)
- **Professional Summary:** Brief introduction (optional)

#### Education
- **Degree:** Select your degree level (Bachelor's, Master's, PhD)
- **Major:** Choose your field of study (30+ options)
- **Specialization:** Specific area of focus (optional)
- **CGPA/GPA:** Academic performance (0-10 scale)

#### Skills & Experience
- **Years of Experience:** Professional work experience (0-20+ years)
- **Skills:** Add technical and soft skills
  - Type skill name
  - Press Enter or click suggestion
  - Supports autocomplete from 100+ skills
- **Certifications:** Add professional certifications
  - Type certification name
  - Press Enter or click suggestion
  - Supports autocomplete from 50+ certifications

#### Social Links
- **LinkedIn:** Your LinkedIn profile URL
- **GitHub:** Your GitHub profile URL
- **Portfolio:** Personal website or portfolio URL

#### Projects (up to 10)
- **Project Title:** Name of the project
- **Description:** Brief overview
- **Technologies Used:** Tech stack
- **Project Link:** Demo or repository URL
- Click "+ Add Project" for additional projects

#### Achievements & Awards
- **Achievement:** Award name or accomplishment
- **Date/Context:** When and where
- Click "+ Add Achievement" for more

#### Languages
- **Language Name:** English, Spanish, etc.
- **Proficiency Level:** Beginner, Intermediate, Advanced, Native
- Click "+ Add Language" for more

#### Save Profile
- Click "Save Changes" button
- Profile saved to localStorage
- Green success notification appears

### 3. Career Prediction

#### Step 1: Navigate to Predict Section
- Click "Predict" in the sidebar
- Or click "Get Career Prediction" from home

#### Step 2: Fill Prediction Form
- **Degree:** Your degree level
- **Major:** Field of study
- **Specialization:** Specific area
- **CGPA:** Academic performance
- **Years of Experience:** Work experience
- **Preferred Industry:** Target industry
- **Skills:** Add relevant skills
- **Certifications:** Add certifications

**Tip:** Use your profile data or customize for different scenarios

#### Step 3: Generate Prediction
- Click "Predict My Career"
- ML model analyzes your profile (takes 1-2 seconds)
- Results appear below

#### Step 4: Analyze Results
The prediction shows:

**Main Prediction Card:**
- **Predicted Role:** Best-fit job title
- **Confidence Score:** Match percentage (0-100%)
- **Confidence Level:** Highly Confident (80%+), Good Match (60-79%), Potential (below 60%)
- **Salary Range:** Expected compensation
- **Growth Rate:** Career growth percentage
- **Market Demand:** Very High, High, Moderate, Low

**Detailed Insights:**

1. **Career Progression Timeline**
   - Entry Level (0-2 years): Salary and skills
   - Mid Level (2-5 years): Advancement path
   - Senior Level (5-8 years): Leadership roles
   - Lead/Principal (8+ years): Executive positions

2. **Skill Assessment Radar Chart**
   - Your Skills vs Required Level
   - 5 dimensions: Tech Skills, Experience, Education, Industry Fit, Soft Skills

3. **Market Position Bar Chart**
   - Your Match vs Market Average
   - Compare with Top 10% Candidates

4. **Missing Skills**
   - Red tags showing skill gaps
   - Prioritized recommendations

5. **Recommended Certifications**
   - Industry-relevant certifications
   - Learning path suggestions

6. **Alternative Career Paths**
   - Top 3 alternative roles
   - Match percentages
   - Market demand indicators
   - Growth rates
   - Reasoning for each

7. **Learning Roadmap**
   - Step-by-step career development plan
   - Timeline and milestones
   - Resource recommendations

8. **A Day in the Life**
   - Typical daily schedule
   - Key responsibilities
   - Work environment

9. **Salary Negotiation Tips**
   - Market research guidance
   - Negotiation strategies
   - Timing advice

10. **Learning Resources**
    - Online courses
    - Certifications
    - Bootcamps

#### Step 5: View History
- Click "History" in sidebar
- See all past predictions
- Search by job title
- Delete old predictions

### 4. Resume Builder

#### Navigate to Resume Builder
- Click "Resume" in sidebar
- Or click "Build Resume" from home

#### Document Type Selection
Choose between:
- **📄 Resume:** Professional resume/CV
- **📝 Cover Letter:** Personalized cover letter

---

#### Creating a Resume

##### Step 1: Choose Template
Select from 3 professional templates:
- **Modern:** Clean, contemporary design with color
- **Classic:** Traditional, ATS-friendly format
- **Creative:** Stand-out design with sidebar

##### Step 2: LinkedIn Import (Optional)
- Paste your LinkedIn profile URL
- Click "Import Data"
- Auto-fills your profile information
- **Note:** Backend API integration required

##### Step 3: Job-Specific Customization (Optional)
**Option A: Paste Job URL**
- Enter job posting URL (LinkedIn, Indeed, etc.)
- Click "Fetch Job"
- Auto-extracts job description
- **Note:** Requires backend scraping API

**Option B: Paste Job Description**
- Copy job description from posting
- Paste into text area
- Click "Customize Resume for This Job"

**Analysis Results:**
- **Match Score:** Your compatibility (0-100%)
- **Missing Skills:** What you need to add
- **Recommendations:** Specific improvements
- **Emphasis Suggestions:** What to highlight

##### Step 4: ATS Score Analysis
- Click "Analyze Current Draft"
- Or upload existing resume to analyze
- Results show:
  - **ATS Score:** 0-100 rating
  - **Keywords Match:** Keyword density
  - **Formatting:** Structure quality
  - **Length:** Page count (ideal: 1-2 pages)
  - **Recommendations:** Improvement tips

##### Step 5: Keyword Optimization
- Enter target job title
- Click "Optimize for ATS"
- Get keyword suggestions
- Click keywords to add to your skills

##### Step 6: Generate Resume
- Click "🎯 Generate Resume"
- Preview appears instantly
- Resume uses your profile data
- All sections automatically populated

##### Step 7: Save Version (Optional)
- Click "💾 Save Current Version"
- Name your version (e.g., "Software Engineer - Google")
- Access later from "Your Resume Versions"
- Manage multiple resume variants

##### Step 8: Download or Email
**Download:**
- Click "⬇️ Download"
- Opens in new tab optimized for printing
- Use browser's Print → Save as PDF
- Print-optimized CSS (no blank space)

**Email:**
- Click "📧 Email Resume"
- Enter recipient email
- Add subject line
- Optional message
- Click "Send Resume"
- **Note:** Requires email API integration

---

#### Creating a Cover Letter

##### Step 1: Switch to Cover Letter Tab
- Click "📝 Cover Letter" tab

##### Step 2: Fill Cover Letter Details
- **Company Name:** Target company (e.g., "Google")
- **Job Title:** Position you're applying for
- **Why This Company?** (Optional): Personalization
- **Tone:** Select writing style
  - **Professional & Formal:** Traditional, corporate
  - **Enthusiastic & Energetic:** Startup, creative
  - **Confident & Bold:** Leadership, senior roles
  - **Humble & Sincere:** Entry-level, career change

##### Step 3: Generate Cover Letter
- Click "✨ Generate Cover Letter"
- AI creates personalized letter
- Uses your profile data
- Includes achievements
- Professional formatting

##### Step 4: Preview & Edit
- Review generated cover letter
- Check for accuracy
- Verify dates and details

##### Step 5: Download or Email
- Same options as resume
- Download as PDF
- Email to recruiter

---

### 5. Resume Tips & Best Practices

#### Resume Content
- **Length:** Keep to 1-2 pages
- **Action Verbs:** Start bullet points with strong verbs
- **Quantify:** Use numbers and metrics
- **Tailor:** Customize for each job application
- **Keywords:** Include job-specific terms
- **Consistency:** Uniform formatting throughout

#### ATS Optimization
- **Standard Sections:** Use conventional headers
- **Simple Formatting:** Avoid tables, columns
- **Keywords:** Match job description terms
- **File Type:** PDF or DOCX
- **Font:** Use standard fonts (Inter, Arial, Calibri)

#### Cover Letter Tips
- **Personalize:** Research the company
- **Match Tone:** Align with company culture
- **Be Specific:** Reference actual job requirements
- **Show Value:** What you bring to the role
- **Call to Action:** Request interview

---

## 🔌 API Documentation

### Base URL
```
http://localhost:8000
```

### Authentication
All protected endpoints require JWT token in Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

### Endpoints

#### 1. **POST** `/register`
Register a new user account.

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

**Errors:**
- `400`: Missing fields or invalid data
- `409`: Username or email already exists

---

#### 2. **POST** `/login`
Authenticate user and get JWT token.

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepass123"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

**Errors:**
- `400`: Missing credentials
- `401`: Invalid username or password

---

#### 3. **POST** `/logout`
Logout user (invalidate token).

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

#### 4. **GET/POST** `/verify-token`
Verify JWT token validity.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "valid": true,
  "user_id": 1
}
```

**Errors:**
- `401`: Invalid or expired token

---

#### 5. **POST** `/api/predict-job`
Generate career prediction using ML model.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "degree": "Bachelors",
  "major": "Computer Science",
  "specialization": "Software Engineering",
  "cgpa": 8.5,
  "years_of_experience": 2,
  "preferred_industry": "IT",
  "skills": "Python,JavaScript,React,Node.js",
  "certifications": "AWS Certified,Google Cloud"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "predicted_role": "Software Engineer",
  "match_percentage": 92,
  "salary_range": "₹8L - ₹15L",
  "growth_rate": "15%",
  "description": "Develops software applications...",
  "skill_gap_analysis": ["Docker", "Kubernetes"],
  "certifications": ["AWS Solutions Architect", "Docker Certified"],
  "roadmap": [
    {
      "step": 1,
      "title": "Foundation Phase",
      "desc": "Master core programming concepts"
    }
  ],
  "top_alternative_roles": [
    {
      "role": "Full Stack Developer",
      "match_percentage": 88,
      "reason": "strong web development skills"
    }
  ]
}
```

**Errors:**
- `400`: Missing required fields
- `401`: Unauthorized
- `500`: Model prediction error

---

#### 6. **GET** `/api/get-options`
Get form dropdown options.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "Degree": ["Bachelors", "Masters", "PhD"],
  "Major": ["Computer Science", "Business", "Engineering", ...],
  "Specialization": ["AI/ML", "Web Development", "Data Science", ...],
  "Preferred Industry": ["IT", "Finance", "Healthcare", ...],
  "Skills": ["Python", "JavaScript", "Java", ...],
  "Certifications": ["AWS Certified", "PMP", "CISSP", ...]
}
```

---

#### 7. **GET** `/api/prediction-history`
Get user's prediction history.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "history": [
    {
      "id": 1,
      "predicted_role": "Software Engineer",
      "match_percentage": 92,
      "timestamp": "2025-11-30T10:30:00",
      "input_data": { ... },
      "prediction_data": { ... }
    }
  ]
}
```

---

#### 8. **GET** `/health`
Health check endpoint.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-30T10:30:00"
}
```

---

### Rate Limits
- **Default:** 100 requests per hour per IP
- **Prediction Endpoint:** 20 requests per hour
- **Auth Endpoints:** 10 requests per 15 minutes

---

## 🧠 ML Model Details

### Model Architecture

**Algorithm:** Logistic Regression (Multi-class)
- **Solver:** lbfgs
- **Max Iterations:** 1000
- **Multi-class:** One-vs-Rest (OvR)
- **Regularization:** L2 (Ridge)

### Training Data
- **Dataset:** `JobRole.csv`
- **Total Samples:** 2,202 career profiles
- **Training Set:** 1,800 samples (81.7%)
- **Test Set:** 402 samples (18.3%)
- **Features:** 181 engineered features
- **Target Classes:** 15 job roles

### Feature Engineering

**Input Features (6):**
1. Degree (categorical)
2. Major (categorical)
3. Specialization (categorical)
4. CGPA (numerical, 0-10)
5. Years of Experience (numerical, 0-20+)
6. Preferred Industry (categorical)
7. Skills (text, comma-separated)
8. Certifications (text, comma-separated)

**Engineered Features (181):**
- **Categorical Encoding:** One-Hot Encoding for Degree, Major, Specialization, Industry (50 features)
- **TF-IDF Vectorization:** Skills and Certifications transformed to 100 text features
- **Numerical Scaling:** StandardScaler for CGPA and Experience (2 features)
- **Interaction Features:** Combined features (29 features)

### Model Performance

**Test Set Metrics:**
- **Accuracy:** 92.3%
- **Precision (Weighted):** 0.91
- **Recall (Weighted):** 0.92
- **F1 Score (Weighted):** 0.89
- **ROC-AUC (Macro):** 0.96

**Per-Class Performance:**
| Job Role | Precision | Recall | F1-Score | Support |
|----------|-----------|--------|----------|---------|
| Software Engineer | 0.95 | 0.94 | 0.94 | 45 |
| Data Scientist | 0.92 | 0.91 | 0.91 | 38 |
| Business Analyst | 0.89 | 0.88 | 0.88 | 32 |
| Marketing Manager | 0.87 | 0.89 | 0.88 | 28 |
| ... | ... | ... | ... | ... |

### Prediction Pipeline

```
User Input → Preprocessing → Feature Engineering → Model Inference → Post-processing → Results
```

**Step 1: Input Validation**
- Check required fields
- Validate data types
- Normalize text inputs

**Step 2: Feature Engineering**
- Encode categorical variables
- Vectorize text features (TF-IDF)
- Scale numerical features
- Create interaction features

**Step 3: Model Inference**
- Pass features to trained model
- Get probability scores for all 15 classes
- Select top prediction and alternatives

**Step 4: Post-processing**
- Map predicted class to job role name
- Calculate confidence score
- Generate skill gap analysis
- Fetch role-specific metadata
- Create learning roadmap
- Format output

**Step 5: Response Generation**
- Build comprehensive JSON response
- Include salary, growth rate, certifications
- Add alternative career paths
- Provide actionable insights

### Model Files

**`best_model.pkl` (1.2 MB):**
- Trained Logistic Regression model
- Serialized with joblib
- Includes model weights and hyperparameters

**`preprocessor.pkl` (450 KB):**
- Complete preprocessing pipeline
- Includes:
  - Label encoders for categorical features
  - TF-IDF vectorizers for text features
  - StandardScaler for numerical features
  - Feature names and column order

**`label_encoders.pkl` (120 KB):**
- Category-to-numeric mappings
- Ensures consistent encoding

**`scaler.pkl` (5 KB):**
- Mean and std for numerical features
- Ensures consistent scaling

**`model_info.json` (15 KB):**
- Model metadata
- Training history
- Performance metrics
- Feature importance
- Class distribution

### Retraining the Model

To retrain with new data:

```bash
# 1. Update JobRole.csv with new samples
# 2. Run training script
python ml/train_model.py

# 3. Restart server to load new model
./stop.sh
./start.sh
```

---

## 🎨 Frontend Features

### Design System

**Color Palette:**
- **Primary:** `#10b981` (Emerald Green)
- **Primary Dark:** `#059669`
- **Background:** `#ffffff` (White)
- **Surface:** `#f9fafb` (Light Gray)
- **Text Main:** `#111827` (Near Black)
- **Text Muted:** `#6b7280` (Gray)
- **Border:** `#e5e7eb` (Light Border)
- **Error:** `#dc2626` (Red)
- **Warning:** `#f59e0b` (Orange)
- **Success:** `#10b981` (Green)
- **Info:** `#3b82f6` (Blue)

**Typography:**
- **Headings:** Space Grotesk (700 weight)
- **Body:** Inter (400, 500, 600 weights)
- **Monospace:** Monospace (for code)

**Spacing Scale:**
- 4px, 8px, 12px, 16px, 20px, 24px, 32px, 40px, 48px

**Border Radius:**
- Small: 6px
- Medium: 12px
- Large: 16px
- Circle: 50%

### Components

**1. Navigation**
- Sidebar navigation with icons
- Active state highlighting
- Mobile-responsive hamburger menu
- User profile dropdown
- Logout functionality

**2. Cards**
- Glassmorphic design
- Hover effects
- Shadow depth
- Consistent padding
- Responsive grid

**3. Forms**
- Input fields with floating labels
- Select dropdowns with styling
- Textarea with auto-resize
- Tag input with autocomplete
- Real-time validation
- Error messages
- Success states

**4. Buttons**
- Primary, Secondary, Outline variants
- Icon buttons
- Loading states
- Disabled states
- Hover/active animations

**5. Modals**
- Overlay with blur
- Centered dialog
- Close on backdrop click
- Escape key support
- Smooth animations

**6. Toast Notifications**
- 4 types: Success, Error, Warning, Info
- Auto-dismiss (4 seconds)
- Slide-in animation
- Close button
- Icon indicators

**7. Charts**
- Radar chart for skill assessment
- Bar chart for market comparison
- Responsive sizing
- Interactive tooltips
- Color-coded data

**8. Tags**
- Skill tags with remove button
- Certification tags
- Keyword suggestion tags
- Color variants
- Hover effects

**9. Timeline**
- Career progression timeline
- Milestone markers
- Animated entrance
- Responsive layout

**10. Tables**
- Alternative careers matrix
- Sortable columns
- Hover row highlighting
- Responsive scrolling

### Responsive Design

**Breakpoints:**
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

**Mobile Optimizations:**
- Hamburger menu
- Stacked layouts
- Touch-friendly buttons (44px minimum)
- Reduced font sizes
- Simplified charts

**Tablet Optimizations:**
- 2-column layouts
- Sidebar collapse
- Optimized spacing

**Desktop Optimizations:**
- Full sidebar
- Multi-column layouts
- Larger charts
- More whitespace

### Performance Optimizations

**1. Code Optimization**
- Minified CSS (inline)
- Compressed images
- Lazy loading for charts
- Debounced search
- Throttled scroll events

**2. Asset Loading**
- CDN for Chart.js
- Google Fonts with display swap
- Preload critical fonts

**3. Caching**
- LocalStorage for profile data
- Browser cache for static assets
- Service worker (future enhancement)

**4. Rendering**
- Virtual DOM patterns
- Batch DOM updates
- CSS animations over JS
- RequestAnimationFrame for smooth animations

### Accessibility

**ARIA Labels:**
- Semantic HTML5 elements
- Role attributes
- ARIA labels for icons
- Alt text for images

**Keyboard Navigation:**
- Tab order optimization
- Focus indicators
- Escape key for modals
- Enter key for forms
- Keyboard shortcuts (Ctrl+P, Ctrl+H, Ctrl+R)

**Screen Reader Support:**
- Descriptive labels
- Form field associations
- Error announcements
- Loading state announcements

**Color Contrast:**
- WCAG AAA compliance
- 7:1 ratio for text
- High contrast mode support

---

## 🔒 Security Features

### Authentication & Authorization

**Password Security:**
- **Hashing:** bcrypt with 12 rounds
- **Salt:** Automatic per-password salt
- **No Plain Text:** Passwords never stored in plain text
- **Strength:** Minimum 6 characters (configurable)

**JWT Tokens:**
- **HS256 Algorithm:** HMAC with SHA-256
- **Expiration:** 24 hours (configurable)
- **Claims:** User ID, username, issued time
- **Refresh:** Automatic on activity (future)
- **Secure Storage:** HTTPOnly cookies (recommended)

**Session Management:**
- **Token Validation:** On every protected request
- **Auto Logout:** On token expiration
- **Logout Endpoint:** Manual logout support

### Input Validation

**Backend Validation:**
- **Type Checking:** Ensure correct data types
- **Length Limits:** Prevent buffer overflow
- **Format Validation:** Email, username patterns
- **SQL Injection Prevention:** Parameterized queries
- **XSS Prevention:** HTML escaping

**Frontend Validation:**
- **Real-time Validation:** As user types
- **Pattern Matching:** Regex for formats
- **Required Fields:** Client-side checks
- **AJAX Validation:** Username availability

### Rate Limiting

**Global Limits:**
- 100 requests per hour per IP
- Protects against DoS attacks

**Endpoint-Specific:**
- `/api/predict-job`: 20 per hour
- `/register`: 10 per 15 minutes
- `/login`: 10 per 15 minutes

**Bypass for Authenticated Users:**
- Higher limits for logged-in users (future)

### CORS Configuration

**Allowed Origins:**
- Frontend URL from environment variable
- Localhost for development
- Production domain for deployment

**Allowed Methods:**
- GET, POST, PUT, DELETE, OPTIONS

**Allowed Headers:**
- Content-Type, Authorization

**Credentials:**
- Support for cookies and auth headers

### Database Security

**SQL Injection Prevention:**
- SQLAlchemy ORM (parameterized queries)
- No raw SQL execution
- Input sanitization

**Data Encryption:**
- Passwords: bcrypt hashing
- Tokens: JWT signing
- Future: Sensitive data encryption at rest

**Access Control:**
- User isolation (can only access own data)
- Role-based access (future: admin roles)

### Environment Security

**Environment Variables:**
- Secrets in `.env` file
- Never committed to Git
- Different configs per environment

**Logging:**
- No sensitive data in logs
- Password redaction
- Rotating log files (5MB limit)
- Secure log storage

### HTTPS (Production)

**Recommended Setup:**
- SSL/TLS certificates (Let's Encrypt)
- HTTPS-only cookies
- HSTS headers
- Secure CSP headers

---

## 🚀 Deployment

### Prerequisites
- Server with Python 3.9+
- Domain name (optional)
- SSL certificate (recommended)
- Database (SQLite or MySQL)

### Option 1: Traditional Server (Linux)

#### Step 1: Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install nginx (optional, for reverse proxy)
sudo apt install nginx -y
```

#### Step 2: Clone and Setup
```bash
# Clone repository
git clone https://github.com/yourusername/edu2job.git
cd edu2job

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 3: Configure Production
```bash
# Create production .env
nano .env
```

```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=YOUR_RANDOM_SECRET_KEY_HERE
JWT_SECRET_KEY=YOUR_JWT_SECRET_HERE
DATABASE_URL=sqlite:///instance/database.db
FRONTEND_URL=https://yourdomain.com
```

#### Step 4: Setup Systemd Service
```bash
sudo nano /etc/systemd/system/edu2job.service
```

```ini
[Unit]
Description=Edu2Job Flask Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/edu2job
Environment="PATH=/path/to/edu2job/.venv/bin"
ExecStart=/path/to/edu2job/.venv/bin/python /path/to/edu2job/backend/app.py

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl start edu2job
sudo systemctl enable edu2job
```

#### Step 5: Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/edu2job
```

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        root /path/to/edu2job/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/edu2job /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

#### Step 6: SSL with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
```

---

### Option 2: Docker Deployment

#### Step 1: Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "backend/app.py"]
```

#### Step 2: Create docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    volumes:
      - ./instance:/app/instance
      - ./logs:/app/logs
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./frontend:/usr/share/nginx/html
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web
    restart: unless-stopped
```

#### Step 3: Deploy
```bash
docker-compose up -d
```

---

### Option 3: Cloud Platforms

#### Heroku
```bash
# Install Heroku CLI
heroku login
heroku create edu2job-app

# Add Procfile
echo "web: python backend/app.py" > Procfile

# Deploy
git push heroku main
```

#### AWS Elastic Beanstalk
```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.9 edu2job

# Create environment
eb create edu2job-env

# Deploy
eb deploy
```

#### Google Cloud Run
```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/edu2job

# Deploy
gcloud run deploy edu2job \
  --image gcr.io/PROJECT_ID/edu2job \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

### Production Checklist

- [ ] Change SECRET_KEY and JWT_SECRET_KEY
- [ ] Set FLASK_ENV=production
- [ ] Disable FLASK_DEBUG
- [ ] Configure production database (MySQL/PostgreSQL)
- [ ] Setup SSL/TLS certificates
- [ ] Enable CORS for production domain
- [ ] Setup logging and monitoring
- [ ] Configure backup strategy
- [ ] Setup CDN for static assets (optional)
- [ ] Configure email service for notifications
- [ ] Setup error tracking (Sentry, etc.)
- [ ] Performance testing and optimization
- [ ] Security audit
- [ ] Documentation for ops team

---

## 🔮 Future Roadmap

### Phase 1: Core Enhancements (Q1 2026)
- [ ] Real PDF generation (jsPDF/pdfmake)
- [ ] More resume templates (10+ total)
- [ ] Backend email sending API
- [ ] LinkedIn OAuth integration
- [ ] Job scraping API
- [ ] Resume analytics dashboard
- [ ] Mobile app (React Native)

### Phase 2: Advanced Features (Q2 2026)
- [ ] Video resume recording
- [ ] AI interview preparation
- [ ] Skill assessment quizzes
- [ ] Resume A/B testing
- [ ] Cover letter variations
- [ ] Job application tracking
- [ ] Recruiter matching
- [ ] Salary negotiation assistant

### Phase 3: Enterprise Features (Q3 2026)
- [ ] Multi-language support
- [ ] Team collaboration
- [ ] University partnerships
- [ ] Bulk student onboarding
- [ ] Analytics for institutions
- [ ] Custom branding (white-label)
- [ ] API for third-party integrations
- [ ] Career counselor portal

### Phase 4: AI Evolution (Q4 2026)
- [ ] GPT-4 integration for predictions
- [ ] Advanced NLP for job matching
- [ ] Personality assessment
- [ ] Career path visualization
- [ ] Market trend prediction
- [ ] Automated job application
- [ ] Interview scheduling bot
- [ ] Success probability prediction

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

1. **Bug Reports:** Found a bug? Open an issue on GitHub
2. **Feature Requests:** Have an idea? We'd love to hear it
3. **Code Contributions:** Submit pull requests
4. **Documentation:** Improve or translate docs
5. **Testing:** Help test new features
6. **Design:** UI/UX improvements
7. **Translations:** Add multi-language support

### Development Setup

```bash
# Fork and clone
git clone https://github.com/yourusername/edu2job.git
cd edu2job

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test
python backend/app.py
# Open frontend/index.html

# Commit and push
git add .
git commit -m "Add your feature"
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

### Code Style

**Python:**
- Follow PEP 8
- Use type hints
- Add docstrings for functions
- Comment complex logic

**JavaScript:**
- Use ES6+ syntax
- Camel case for variables
- Comment non-obvious code
- Keep functions small and focused

**HTML/CSS:**
- Semantic HTML5
- BEM naming for CSS
- Indent with 2 spaces
- Responsive by default

### Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Edu2Job Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Support & Contact

### Get Help
- **Documentation:** You're reading it!
- **GitHub Issues:** Report bugs or request features
- **Email:** support@edu2job.com
- **Discord:** Join our community server
- **Twitter:** @edu2job

### FAQ

**Q: Is Edu2Job free to use?**
A: Yes, the current version is completely free and open-source.

**Q: Can I self-host Edu2Job?**
A: Absolutely! Follow the deployment guide above.

**Q: How accurate are the career predictions?**
A: Our ML model has 92%+ accuracy on test data, but remember it's a guidance tool, not absolute truth.

**Q: Can I use my own resume template?**
A: Currently, we have 3 built-in templates. Custom templates are on the roadmap.

**Q: Is my data secure?**
A: Yes, we use industry-standard security (bcrypt, JWT, HTTPS). Data is isolated per user.

**Q: Can I export my data?**
A: Yes, you can download your resume. Full profile export is coming soon.

**Q: Does it work offline?**
A: Partially. Profile data is cached locally, but predictions require server connection.

**Q: Can I contribute?**
A: Yes! See the Contributing section above.

---

## 🙏 Acknowledgments

### Technologies Used
- Flask framework by Pallets Projects
- scikit-learn by the scikit-learn developers
- Chart.js by Chart.js contributors
- Icons from Heroicons
- Fonts from Google Fonts

### Inspiration
- Career guidance counselors
- Job seekers and students worldwide
- Open-source community

### Special Thanks
- All contributors and testers
- Early adopters and feedback providers
- Universities partnering with us

---

## 📊 Project Stats

- **Lines of Code:** 8,000+
- **Commits:** 150+
- **Contributors:** 5
- **Stars:** ⭐ Give us a star on GitHub!
- **Forks:** Fork and contribute!

---

## 🎉 Changelog

### Version 2.0.0 (December 1, 2025)
- ✨ Added Cover Letter Generator
- ✨ Added Job-Specific Resume Customizer
- ✨ Added LinkedIn Import (UI)
- ✨ Added Email Resume Feature (UI)
- ✨ Document type tabs (Resume/Cover Letter)
- 🎨 Redesigned ATS Analyzer with better colors
- 🐛 Fixed template literal syntax error
- 🐛 Fixed resume print blank space issue
- 📚 Complete documentation overhaul

### Version 1.5.0 (November 28, 2025)
- ✨ Added ATS Score Analyzer
- ✨ Added Resume Version Manager
- ✨ Added Keyword Optimizer
- ✨ Projects, Achievements, Languages sections in Profile
- ✨ Social links (LinkedIn, GitHub, Portfolio)
- 🎨 Changed profile layout to vertical
- 🐛 Fixed multiple onclick handlers
- 🔒 Enhanced security with rate limiting

### Version 1.0.0 (November 20, 2025)
- 🎉 Initial release
- ✨ ML-powered career prediction
- ✨ Basic resume builder (3 templates)
- ✨ User authentication
- ✨ Profile management
- ✨ Prediction history

---

## 📱 Screenshots

### Landing Page
*Clean, modern landing page with clear call-to-action*

### Dashboard Home
*Overview with profile completion, quick actions, and statistics*

### Career Prediction
*Detailed prediction results with charts and insights*

### Resume Builder
*Professional resume templates with live preview*

### Cover Letter Generator
*AI-powered cover letter creation*

---

**Made with ❤️ by the Edu2Job Team**

*Empowering careers through AI and innovation*

---

**Last Updated:** December 1, 2025  
**Version:** 2.0.0  
**Status:** ✅ Production Ready
