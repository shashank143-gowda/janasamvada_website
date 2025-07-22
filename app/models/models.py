from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(15))
    village = db.Column(db.String(100))
    district = db.Column(db.String(100))
    state = db.Column(db.String(100))
    reward_points = db.Column(db.Integer, default=0)
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'
    language_preference = db.Column(db.String(10), default='en')  # 'en' or 'kn'
    profile_image = db.Column(db.String(200))
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def is_admin(self):
        return self.role == 'admin'

class PublicService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)  # hospital, school, transport, etc.
    address = db.Column(db.String(200), nullable=False)
    contact = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    district = db.Column(db.String(100))
    state = db.Column(db.String(100))

class GovernmentScheme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # health, agriculture, women, etc.
    description = db.Column(db.Text, nullable=False)
    eligibility = db.Column(db.Text, nullable=False)
    application_process = db.Column(db.Text, nullable=False)
    documents_required = db.Column(db.Text)
    contact_info = db.Column(db.String(200))
    website = db.Column(db.String(200))

class Hazard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    hazard_type = db.Column(db.String(50), nullable=False)  # road, water, electricity, etc.
    image_path = db.Column(db.String(200))
    video_path = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    location_description = db.Column(db.String(200))
    status = db.Column(db.String(20), default='pending')  # pending, in-progress, resolved
    upvotes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('hazards', lazy=True))

class CorruptionReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    date_of_incident = db.Column(db.Date, nullable=False)
    evidence_path = db.Column(db.String(200))
    status = db.Column(db.String(20), default='under review')  # under review, investigating, resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TreePlanting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tree_type = db.Column(db.String(100))
    image_path = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    location_description = db.Column(db.String(200))
    status = db.Column(db.String(20), default='pending')  # pending, verified, rejected
    points_awarded = db.Column(db.Integer, default=0)
    verified_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('tree_plantings', lazy=True))
    verifier = db.relationship('User', foreign_keys=[verified_by], backref=db.backref('verifications', lazy=True))

class ClimateInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    temperature = db.Column(db.Float)
    weather_condition = db.Column(db.String(50))  # sunny, rainy, cloudy, etc.
    rainfall_prediction = db.Column(db.String(100))
    farming_tip = db.Column(db.Text)
    region = db.Column(db.String(100))

class RewardRedemption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    points_redeemed = db.Column(db.Integer, nullable=False)
    reward_type = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, processed, delivered
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('redemptions', lazy=True))

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(200))
    category = db.Column(db.String(50))  # local, national, government, etc.
    region = db.Column(db.String(100))  # For location-based news
    source = db.Column(db.String(100))
    source_url = db.Column(db.String(200))
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_featured = db.Column(db.Boolean, default=False)
    
class ChatbotQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    query = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(10), default='en')  # Language code
    voice_input = db.Column(db.Boolean, default=False)  # Whether the query was via voice
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    feedback = db.Column(db.Boolean, nullable=True)  # True for positive, False for negative
    
    user = db.relationship('User', backref=db.backref('chatbot_queries', lazy=True))

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    feedback_type = db.Column(db.String(50))  # general, bug, feature, etc.
    content = db.Column(db.Text, nullable=False)
    page = db.Column(db.String(100))  # Which page the feedback was submitted from
    rating = db.Column(db.Integer)  # 1-5 rating
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('feedback', lazy=True))