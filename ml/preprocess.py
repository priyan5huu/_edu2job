"""
Edu2Job - Data Preprocessing Pipeline
=====================================
Handles all data cleaning, feature engineering, encoding, and scaling.
This module ensures data consistency between training and inference.

Author: ML Pipeline Generator
Date: 2025
"""

import pandas as pd
import re
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import logging
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import ssl
import os
import certifi

# Fix for SSL certificate verify failed error on Mac
# This is a common issue where Python doesn't have access to system certificates
try:
    # Option 1: Use certifi's certificate bundle (Best practice)
    os.environ['SSL_CERT_FILE'] = certifi.where()
    ssl._create_default_https_context = ssl.create_default_context
except Exception:
    # Option 2: Fallback to unverified context (Works if certifi fails)
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    try:
        nltk.download('punkt', quiet=True)
    except:
        print("⚠️  Could not download NLTK punkt data")

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    try:
        nltk.download('wordnet', quiet=True)
    except:
        print("⚠️  Could not download NLTK wordnet data")

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    try:
        nltk.download('stopwords', quiet=True)
    except:
        print("⚠️  Could not download NLTK stopwords data")

# Initialize NLTK components with fallbacks
try:
    stop_words = set(stopwords.words('english'))
except:
    stop_words = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"])

lemmatizer = None
try:
    lemmatizer = WordNetLemmatizer()
except Exception as e:
    print(f"⚠️  Could not initialize WordNetLemmatizer: {e}")
    lemmatizer = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Edu2JobPreprocessor:
    """
    Comprehensive preprocessing pipeline for Edu2Job prediction model.
    Handles missing values, outliers, text cleaning, encoding, and scaling.
    """
    
    def __init__(self):
        """Initialize preprocessing components"""
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.skills_vectorizer = TfidfVectorizer(
            max_features=100,  # Increased from 50
            ngram_range=(1, 2),
            min_df=2,
            stop_words='english'
        )
        self.cert_vectorizer = TfidfVectorizer(
            max_features=50,
            ngram_range=(1, 2),
            min_df=2,
            stop_words='english'
        )
        self.lemmatizer = lemmatizer
        self.stop_words = stop_words
        self.is_fitted = False
        
        # Enhanced skill categorization with role-specific distinctions
        self.skill_categories = {
            'cloud_infrastructure': [
                'aws', 'azure', 'gcp', 'kubernetes', 'docker', 'terraform', 'ansible', 'jenkins',
                'ci/cd', 'devops', 'linux', 'ubuntu', 'centos', 'infrastructure', 'deployment',
                'containers', 'orchestration', 'virtualization', 'scalability', 'monitoring'
            ],
            'data_analysis': [
                'sql', 'excel', 'tableau', 'power bi', 'statistics', 'data visualization',
                'reporting', 'dashboard', 'business intelligence', 'etl', 'data warehousing',
                'data mining', 'analytics', 'metrics', 'kpi', 'forecasting'
            ],
            'data_science': [
                'python', 'r', 'machine learning', 'deep learning', 'tensorflow', 'pytorch',
                'pandas', 'numpy', 'matplotlib', 'seaborn', 'scikit-learn', 'jupyter',
                'modeling', 'algorithms', 'statistics', 'predictive analytics'
            ],
            'programming': [
                'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'scala',
                'typescript', 'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express',
                'django', 'flask', 'spring', 'hibernate', '.net', 'asp.net', 'api development'
            ],
            'web_development': [
                'html', 'css', 'javascript', 'react', 'angular', 'vue', 'node.js', 'express',
                'django', 'flask', 'php', 'wordpress', 'bootstrap', 'jquery', 'sass', 'less',
                'responsive design', 'frontend', 'backend', 'full stack'
            ],
            'design_ui_ux': [
                'photoshop', 'illustrator', 'figma', 'sketch', 'adobe', 'ui/ux', 'user experience',
                'user interface', 'graphic design', 'prototyping', 'wireframing', 'canva',
                'usability', 'user research', 'interaction design'
            ],
            'business_management': [
                'excel', 'powerpoint', 'word', 'project management', 'agile', 'scrum', 'kanban',
                'jira', 'confluence', 'stakeholder management', 'requirements gathering',
                'business analysis', 'product management', 'roadmap', 'strategy'
            ],
            'security': [
                'cybersecurity', 'network security', 'encryption', 'firewall', 'penetration testing',
                'vulnerability assessment', 'siem', 'ids', 'ips', 'compliance', 'gdpr', 'iso 27001',
                'security audits', 'risk assessment'
            ],
            'finance_accounting': [
                'financial analysis', 'budgeting', 'forecasting', 'valuation', 'risk management',
                'investment banking', 'accounting', 'sap', 'oracle financials', 'quickbooks',
                'financial modeling', 'portfolio management'
            ],
            'database_bigdata': [
                'mysql', 'postgresql', 'mongodb', 'big data', 'hadoop', 'spark', 'kafka',
                'airflow', 'data lake', 'data pipeline', 'nosql', 'database design'
            ]
        }
        
        # Role-specific keywords with weights for better distinction
        self.role_keywords = {
            'Cloud Engineer': {
                'high_priority': ['aws', 'azure', 'gcp', 'kubernetes', 'docker', 'terraform', 'devops', 'ci/cd', 'infrastructure', 'deployment', 'containers', 'orchestration'],
                'medium_priority': ['linux', 'monitoring', 'scalability', 'virtualization', 'cloud architecture'],
                'weight': 3.0
            },
            'Data Analyst': {
                'high_priority': ['sql', 'tableau', 'power bi', 'excel', 'statistics', 'data visualization', 'reporting', 'dashboard', 'business intelligence', 'etl'],
                'medium_priority': ['python', 'r', 'pandas', 'data analysis', 'metrics', 'kpi'],
                'weight': 2.5
            },
            'Data Scientist': {
                'high_priority': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'python', 'r', 'statistics', 'modeling', 'predictive analytics'],
                'medium_priority': ['pandas', 'numpy', 'scikit-learn', 'jupyter', 'algorithms'],
                'weight': 2.8
            },
            'Software Developer': {
                'high_priority': ['java', 'javascript', 'c++', 'git', 'algorithms', 'data structures', 'oop', 'api development', 'software engineering'],
                'medium_priority': ['programming', 'coding', 'debugging', 'testing', 'version control'],
                'weight': 2.0
            },
            'Web Developer': {
                'high_priority': ['html', 'css', 'javascript', 'react', 'angular', 'vue', 'node.js', 'responsive design', 'frontend', 'backend'],
                'medium_priority': ['bootstrap', 'jquery', 'sass', 'full stack', 'web development'],
                'weight': 2.2
            },
            'UI/UX Designer': {
                'high_priority': ['figma', 'sketch', 'adobe', 'prototyping', 'user research', 'usability testing', 'design systems', 'user experience'],
                'medium_priority': ['photoshop', 'illustrator', 'wireframing', 'interaction design'],
                'weight': 2.5
            },
            'Cyber Security Analyst': {
                'high_priority': ['penetration testing', 'vulnerability assessment', 'network security', 'encryption', 'firewall', 'compliance', 'cybersecurity'],
                'medium_priority': ['risk assessment', 'security audits', 'siem', 'ids', 'ips'],
                'weight': 2.8
            },
            'Business Analyst': {
                'high_priority': ['requirements gathering', 'stakeholder management', 'business process', 'use cases', 'business analysis'],
                'medium_priority': ['agile', 'scrum', 'documentation', 'process improvement'],
                'weight': 2.0
            },
            'Product Manager': {
                'high_priority': ['roadmap', 'product strategy', 'user stories', 'backlog management', 'market research', 'product management'],
                'medium_priority': ['stakeholder management', 'requirements', 'prioritization'],
                'weight': 2.3
            },
            'ML Engineer': {
                'high_priority': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'mlops', 'model deployment', 'production ml'],
                'medium_priority': ['kubernetes', 'docker', 'monitoring', 'scalability', 'model serving'],
                'weight': 3.0
            },
            'Financial Analyst': {
                'high_priority': ['financial analysis', 'budgeting', 'forecasting', 'valuation', 'investment analysis', 'financial modeling'],
                'medium_priority': ['excel', 'accounting', 'risk management', 'portfolio management'],
                'weight': 2.2
            },
            'Marketing Analyst': {
                'high_priority': ['marketing analytics', 'campaign analysis', 'seo', 'social media', 'conversion rate', 'a/b testing'],
                'medium_priority': ['google analytics', 'marketing metrics', 'customer insights'],
                'weight': 2.0
            },
            'Content Strategist': {
                'high_priority': ['content strategy', 'seo', 'content management', 'copywriting', 'brand voice', 'content marketing'],
                'medium_priority': ['blogging', 'social media', 'editorial', 'content creation'],
                'weight': 2.0
            },
            'Graphic Designer': {
                'high_priority': ['photoshop', 'illustrator', 'branding', 'print design', 'typography', 'color theory', 'graphic design'],
                'medium_priority': ['adobe', 'creative', 'visual design', 'layout'],
                'weight': 2.0
            },
            'Academic Instructor/Lecturer': {
                'high_priority': ['teaching', 'curriculum development', 'academic research', 'student assessment', 'pedagogy', 'education'],
                'medium_priority': ['mentoring', 'course design', 'academic writing', 'instructional design'],
                'weight': 2.0
            }
        }
        
        # Categorical columns that need label encoding
        self.categorical_cols = [
            'Degree',
            'Major', 
            'Specialization',
            'Preferred Industry'
        ]
        
        # Numerical columns that need scaling
        self.numerical_cols = ['CGPA', 'Years of Experience']
        
        # Text columns for TF-IDF
        self.text_cols = ['Skills', 'Certification']
        
        logger.info("✅ Preprocessor initialized")
    
    def clean_text(self, text):
        """
        Clean and normalize text data with lemmatization.
        
        Args:
            text: Input text string
            
        Returns:
            Cleaned text string
        """
        if pd.isna(text) or text is None:
            return ''
        
        text = str(text).lower()
        # Remove special characters but keep spaces and common punctuation
        text = re.sub(r'[^a-z0-9\s,\.]', ' ', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Tokenize and lemmatize
        tokens = text.split()
        lemmatized_tokens = []
        for token in tokens:
            if token not in self.stop_words and len(token) > 2:
                if self.lemmatizer:
                    try:
                        lemma = self.lemmatizer.lemmatize(token)
                    except:
                        lemma = token
                else:
                    lemma = token
                lemmatized_tokens.append(lemma)
        
        return ' '.join(lemmatized_tokens)
    
    def categorize_skills(self, skills_text):
        """
        Categorize skills into predefined categories.
        
        Args:
            skills_text: Cleaned skills text
            
        Returns:
            Dictionary of skill category counts
        """
        if not skills_text:
            return {cat: 0 for cat in self.skill_categories.keys()}
        
        skills_lower = skills_text.lower()
        category_counts = {}
        
        for category, keywords in self.skill_categories.items():
            count = 0
            for keyword in keywords:
                if keyword in skills_lower:
                    count += 1
            category_counts[category] = count
        
        return category_counts
    
    def extract_role_features(self, skills_text, cert_text):
        """
        Extract role-specific features based on weighted keywords.
        
        Args:
            skills_text: Cleaned skills text
            cert_text: Cleaned certification text
            
        Returns:
            Dictionary of role-specific feature scores
        """
        combined_text = f"{skills_text} {cert_text}".lower()
        role_features = {}
        
        for role, keyword_config in self.role_keywords.items():
            high_priority = keyword_config['high_priority']
            medium_priority = keyword_config.get('medium_priority', [])
            weight = keyword_config.get('weight', 1.0)
            
            # Calculate score based on keyword matches
            high_score = sum(1 for keyword in high_priority if keyword in combined_text)
            medium_score = sum(0.5 for keyword in medium_priority if keyword in combined_text)
            
            total_score = (high_score + medium_score) * weight
            
            # Normalize by maximum possible score for this role
            max_possible = (len(high_priority) + len(medium_priority) * 0.5) * weight
            normalized_score = total_score / max_possible if max_possible > 0 else 0
            
            role_features[f"{role.lower().replace(' ', '_')}_score"] = min(normalized_score, 1.0)  # Cap at 1.0
        
        return role_features
    
    def normalize_cgpa(self, cgpa):
        """
        Normalize CGPA to 10-point scale.
        Handles US GPA (4.0 scale) and percentage conversions.
        
        Args:
            cgpa: CGPA value (can be on 4.0 scale, 10.0 scale, or percentage)
            
        Returns:
            Normalized CGPA on 10-point scale
        """
        try:
            cgpa_float = float(cgpa)
            
            # Handle 4-point scale (US GPA)
            if 0 < cgpa_float <= 4.5:
                # Convert 4-point to 10-point scale
                normalized = (cgpa_float / 4.0) * 10.0
                return round(normalized, 2)
            
            # Handle 10-point scale
            elif 4.5 < cgpa_float <= 10.0:
                return round(cgpa_float, 2)
            
            # Handle percentage scale
            elif cgpa_float > 10:
                normalized = cgpa_float / 10.0
                return min(round(normalized, 2), 10.0)
            
            else:
                # Invalid CGPA, return median value
                logger.warning(f"Invalid CGPA: {cgpa}, using median 7.5")
                return 7.5
                
        except (ValueError, TypeError):
            logger.warning(f"Cannot convert CGPA: {cgpa}, using median 7.5")
            return 7.5
    
    def handle_missing_values(self, df):
        """
        Handle missing values intelligently for each column type.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with missing values handled
        """
        df = df.copy()
        
        # Handle Certification: 'None' for missing
        if 'Certification' in df.columns:
            df['Certification'] = df['Certification'].fillna('None')
            df.loc[df['Certification'].str.strip() == '', 'Certification'] = 'None'
        
        # Handle Specialization: 'General' for missing
        if 'Specialization' in df.columns:
            df['Specialization'] = df['Specialization'].fillna('General')
            df.loc[df['Specialization'].str.strip() == '', 'Specialization'] = 'General'
        
        # Handle numerical: median imputation
        for col in self.numerical_cols:
            if col in df.columns:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
        
        # Handle categorical: mode imputation
        for col in self.categorical_cols:
            if col in df.columns and df[col].isna().any():
                mode_val = df[col].mode()[0] if len(df[col].mode()) > 0 else 'Unknown'
                df[col] = df[col].fillna(mode_val)
        
        logger.info("✅ Missing values handled")
        return df
    
    def remove_outliers(self, df, columns=None):
        """
        Remove outliers using IQR method.
        
        Args:
            df: Input DataFrame
            columns: List of columns to check for outliers (default: numerical_cols)
            
        Returns:
            DataFrame with outliers removed
        """
        if columns is None:
            columns = self.numerical_cols
        
        df_clean = df.copy()
        initial_count = len(df_clean)
        
        for col in columns:
            if col not in df_clean.columns:
                continue
                
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            
            # Remove outliers
            df_clean = df_clean[
                (df_clean[col] >= lower) & (df_clean[col] <= upper)
            ]
        
        removed_count = initial_count - len(df_clean)
        logger.info(f"✅ Removed {removed_count} outliers ({removed_count/initial_count*100:.1f}%)")
        
        return df_clean
    
    def fit(self, df):
        """
        Fit preprocessor on training data.
        Learns encoders, scalers, and vectorizers.
        
        Args:
            df: Training DataFrame with all required columns
        """
        logger.info("🔧 Fitting preprocessor on training data...")
        
        df = df.copy()
        
        # 1. Handle missing values
        df = self.handle_missing_values(df)
        
        # 2. Normalize CGPA
        if 'CGPA' in df.columns:
            df['CGPA'] = df['CGPA'].apply(self.normalize_cgpa)
        
        # 3. Remove outliers
        df = self.remove_outliers(df)
        
        # 4. Clean text columns
        for col in self.text_cols:
            if col in df.columns:
                df[col] = df[col].apply(self.clean_text)
        
        # 5. Fit label encoders for categorical columns
        for col in self.categorical_cols:
            if col in df.columns:
                le = LabelEncoder()
                le.fit(df[col])
                self.label_encoders[col] = le
                logger.info(f"  ✓ {col}: {len(le.classes_)} unique values")
        
        # 6. Fit TF-IDF vectorizers for text columns
        if 'Skills' in df.columns:
            self.skills_vectorizer.fit(df['Skills'])
            logger.info(f"  ✓ Skills TF-IDF: {len(self.skills_vectorizer.get_feature_names_out())} features")
        
        if 'Certification' in df.columns:
            self.cert_vectorizer.fit(df['Certification'])
            logger.info(f"  ✓ Certification TF-IDF: {len(self.cert_vectorizer.get_feature_names_out())} features")
        
        # 7. Fit scaler on numerical columns
        if all(col in df.columns for col in self.numerical_cols):
            # First encode categoricals to get complete feature set
            df_encoded = df.copy()
            for col in self.categorical_cols:
                if col in df_encoded.columns:
                    df_encoded[col] = self.label_encoders[col].transform(df_encoded[col])
            
            # Now fit scaler on numerical columns
            self.scaler.fit(df_encoded[self.numerical_cols])
            logger.info(f"  ✓ Scaler fitted on {self.numerical_cols}")
        
        self.is_fitted = True
        logger.info("✅ Preprocessor fitting complete!")
        
        return df
    
    def transform(self, df, is_training=False):
        """
        Transform data using fitted preprocessor.
        
        Args:
            df: Input DataFrame
            is_training: If True, includes target column and removes outliers
            
        Returns:
            Transformed DataFrame ready for model
        """
        if not self.is_fitted:
            raise ValueError("Preprocessor must be fitted before transform. Call fit() first.")
        
        logger.info(f"🔄 Transforming data (training={is_training})...")
        
        df = df.copy()
        
        # 1. Handle missing values
        df = self.handle_missing_values(df)
        
        # 2. Normalize CGPA
        if 'CGPA' in df.columns:
            df['CGPA'] = df['CGPA'].apply(self.normalize_cgpa)
        
        # 3. Remove outliers (only during training)
        if is_training:
            df = self.remove_outliers(df)
        
        # 4. Clean text columns
        for col in self.text_cols:
            if col in df.columns:
                df[col] = df[col].apply(self.clean_text)
        
        # 5. Transform categorical columns using label encoders
        for col in self.categorical_cols:
            if col in df.columns:
                # Handle unseen categories by mapping to most common class
                le = self.label_encoders[col]
                most_common_class = le.classes_[0]
                
                # Map unseen values to most common
                df[col] = df[col].apply(
                    lambda x: x if x in le.classes_ else most_common_class
                )
                df[col] = le.transform(df[col])
        
        # 6. Transform text columns using TF-IDF and extract additional features
        skills_features = None
        cert_features = None
        skill_category_features = None
        role_features = None
        
        if 'Skills' in df.columns:
            # TF-IDF features
            skills_tfidf = self.skills_vectorizer.transform(df['Skills'])
            skills_features = pd.DataFrame(
                skills_tfidf.toarray(),
                columns=[f'skill_{i}' for i in range(skills_tfidf.shape[1])],
                index=df.index
            )
            
            # Skill category features
            skill_categories = df['Skills'].apply(self.categorize_skills)
            skill_category_features = pd.DataFrame(list(skill_categories), index=df.index)
        
        if 'Certification' in df.columns:
            cert_tfidf = self.cert_vectorizer.transform(df['Certification'])
            cert_features = pd.DataFrame(
                cert_tfidf.toarray(),
                columns=[f'cert_{i}' for i in range(cert_tfidf.shape[1])],
                index=df.index
            )
        
        # Role-specific features
        if 'Skills' in df.columns and 'Certification' in df.columns:
            role_scores = []
            for idx, row in df.iterrows():
                role_feat = self.extract_role_features(row['Skills'], row['Certification'])
                role_scores.append(role_feat)
            role_features = pd.DataFrame(role_scores, index=df.index)
        
        # 7. Scale numerical features
        if all(col in df.columns for col in self.numerical_cols):
            df[self.numerical_cols] = self.scaler.transform(df[self.numerical_cols])
        
        # 8. Combine all features
        # Drop original text columns and combine with all feature types
        feature_cols = self.categorical_cols + self.numerical_cols
        df_features = df[feature_cols].copy()
        
        if skills_features is not None:
            df_features = pd.concat([df_features, skills_features], axis=1)
        
        if cert_features is not None:
            df_features = pd.concat([df_features, cert_features], axis=1)
        
        if skill_category_features is not None:
            df_features = pd.concat([df_features, skill_category_features], axis=1)
        
        if role_features is not None:
            df_features = pd.concat([df_features, role_features], axis=1)
        
        # Keep target if training
        if is_training and 'Job Role' in df.columns:
            # Encode target
            if 'Job Role' not in self.label_encoders:
                le_target = LabelEncoder()
                le_target.fit(df['Job Role'])
                self.label_encoders['Job Role'] = le_target
            
            y = self.label_encoders['Job Role'].transform(df['Job Role'])
            logger.info(f"✅ Transformed {len(df_features)} samples, {len(df_features.columns)} features")
            return df_features, y
        
        logger.info(f"✅ Transformed {len(df_features)} samples, {len(df_features.columns)} features")
        return df_features
    
    def fit_transform(self, df):
        """
        Fit and transform training data in one step.
        
        Args:
            df: Training DataFrame with target column
            
        Returns:
            Tuple of (X, y) - features and target
        """
        self.fit(df)
        return self.transform(df, is_training=True)
    
    def save(self, filepath='preprocessor.pkl'):
        """
        Save fitted preprocessor to disk.
        
        Args:
            filepath: Path to save preprocessor
        """
        if not self.is_fitted:
            raise ValueError("Cannot save unfitted preprocessor")
        
        joblib.dump(self, filepath)
        logger.info(f"💾 Preprocessor saved to {filepath}")
    
    @staticmethod
    def load(filepath='preprocessor.pkl'):
        """
        Load fitted preprocessor from disk.
        
        Args:
            filepath: Path to saved preprocessor
            
        Returns:
            Loaded Edu2JobPreprocessor instance
        """
        preprocessor = joblib.load(filepath)
        logger.info(f"📂 Preprocessor loaded from {filepath}")
        return preprocessor
    
    def get_feature_names(self):
        """
        Get list of all feature names after transformation.
        
        Returns:
            List of feature names
        """
        feature_names = self.categorical_cols + self.numerical_cols
        
        if hasattr(self.skills_vectorizer, 'get_feature_names_out'):
            feature_names += [f'skill_{i}' for i in range(len(self.skills_vectorizer.get_feature_names_out()))]
        
        if hasattr(self.cert_vectorizer, 'get_feature_names_out'):
            feature_names += [f'cert_{i}' for i in range(len(self.cert_vectorizer.get_feature_names_out()))]
        
        # Add skill category features
        feature_names += list(self.skill_categories.keys())
        
        # Add role-specific features
        feature_names += [f"{role.lower().replace(' ', '_')}_score" for role in self.role_keywords.keys()]
        
        return feature_names


if __name__ == '__main__':
    # Test preprocessing pipeline
    print("="*60)
    print("Testing Edu2Job Preprocessing Pipeline")
    print("="*60)
    
    # Load sample data
    try:
        df = pd.read_csv('../JobRole.csv')
        print(f"\n✅ Loaded dataset: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        
        # Initialize and fit preprocessor
        preprocessor = Edu2JobPreprocessor()
        X, y = preprocessor.fit_transform(df)
        
        print(f"\n✅ Preprocessing complete!")
        print(f"   Features shape: {X.shape}")
        print(f"   Target shape: {y.shape}")
        print(f"   Feature names: {len(preprocessor.get_feature_names())}")
        
        # Save preprocessor
        preprocessor.save('../preprocessor.pkl')
        
        # Test single prediction
        print("\n" + "="*60)
        print("Testing single sample transformation")
        print("="*60)
        
        sample_input = pd.DataFrame([{
            'Degree': 'B.Tech',
            'Major': 'Computer Science',
            'Specialization': 'Machine Learning',
            'CGPA': 8.5,
            'Skills': 'Python, Machine Learning, TensorFlow, Deep Learning',
            'Certification': 'AWS Certified, Google Cloud',
            'Years of Experience': 2,
            'Preferred Industry': 'Tech'
        }])
        
        X_sample = preprocessor.transform(sample_input, is_training=False)
        print(f"✅ Sample transformed: {X_sample.shape}")
        print(f"   Features: {X_sample.iloc[0, :10].to_dict()}")  # Show first 10 features
        
    except FileNotFoundError:
        print("❌ JobRole.csv not found. Please ensure dataset is in parent directory.")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
