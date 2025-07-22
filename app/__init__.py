from flask import Flask, render_template
from flask_cors import CORS
from config import Config
from app.models.models import db
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.services import services_bp
    from app.routes.schemes import schemes_bp
    from app.routes.hazards import hazards_bp
    from app.routes.corruption import corruption_bp
    from app.routes.climate import climate_bp
    from app.routes.trees import trees_bp
    from app.routes.admin import admin_bp
    from app.routes.translator import translator_bp
    from app.routes.dhvani import dhvani_bp
    from app.routes.speech import speech_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(services_bp, url_prefix='/services')
    app.register_blueprint(schemes_bp, url_prefix='/schemes')
    app.register_blueprint(hazards_bp, url_prefix='/hazards')
    app.register_blueprint(corruption_bp, url_prefix='/corruption')
    app.register_blueprint(climate_bp, url_prefix='/climate')
    app.register_blueprint(trees_bp, url_prefix='/trees')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(translator_bp, url_prefix='/translator')
    app.register_blueprint(dhvani_bp, url_prefix='/dhvani')
    app.register_blueprint(speech_bp, url_prefix='/speech')
    
    # Include chatbot in all templates
    @app.context_processor
    def inject_chatbot():
        return dict(include_chatbot=True)
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    # Add language translation support
    @app.context_processor
    def inject_language_support():
        return dict(include_translator=True)
    
    return app