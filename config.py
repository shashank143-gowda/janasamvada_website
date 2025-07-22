import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jansamvaad-secret-key'
    
    # Use SQLite instead of MySQL
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'wav', 'mp3', 'ogg'}
    
    # Dhvani.ai API configuration
    DHVANI_API_KEY = os.environ.get('DHVANI_API_KEY') or 'shashanksmv511@gmail_dwani.com'
    DHVANI_BASE_URL = os.environ.get('DHVANI_BASE_URL') or 'https://dwani-dwani-api.hf.space'