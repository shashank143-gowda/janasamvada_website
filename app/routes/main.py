from flask import Blueprint, render_template, jsonify
from app.models.models import db, User, PublicService, GovernmentScheme, Hazard, ClimateInfo

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', include_chatbot=True)

@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/api/stats')
def get_stats():
    """Get basic statistics for the dashboard"""
    try:
        user_count = User.query.count()
        service_count = PublicService.query.count()
        scheme_count = GovernmentScheme.query.count()
        hazard_count = Hazard.query.count()
        
        # Get latest climate info
        climate = ClimateInfo.query.order_by(ClimateInfo.date.desc()).first()
        climate_data = None
        if climate:
            climate_data = {
                'temperature': climate.temperature,
                'condition': climate.weather_condition,
                'rainfall': climate.rainfall_prediction,
                'tip': climate.farming_tip
            }
        
        return jsonify({
            'success': True,
            'data': {
                'users': user_count,
                'services': service_count,
                'schemes': scheme_count,
                'hazards': hazard_count,
                'climate': climate_data
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500