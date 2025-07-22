from flask import Blueprint, request, jsonify, render_template, current_app
from app.models.models import db, ClimateInfo
from datetime import datetime, timedelta
import requests
import os

climate_bp = Blueprint('climate_bp', __name__)

# OpenWeatherMap API configuration
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/"

def get_weather_condition(weather_id):
    """Map OpenWeatherMap weather ID to our weather condition format"""
    # Thunderstorm
    if 200 <= weather_id < 300:
        return "Heavy Rain"
    # Drizzle
    elif 300 <= weather_id < 400:
        return "Light Rain"
    # Rain
    elif 500 <= weather_id < 600:
        if weather_id < 502:
            return "Light Rain"
        else:
            return "Heavy Rain"
    # Snow
    elif 600 <= weather_id < 700:
        return "Snowy"
    # Atmosphere (fog, mist, etc.)
    elif 700 <= weather_id < 800:
        return "Cloudy"
    # Clear
    elif weather_id == 800:
        return "Sunny"
    # Clouds
    elif 801 <= weather_id < 900:
        if weather_id == 801:
            return "Partly Cloudy"
        else:
            return "Cloudy"
    else:
        return "Partly Cloudy"

def get_rainfall_prediction(weather_id):
    """Generate rainfall prediction based on weather ID"""
    # Thunderstorm
    if 200 <= weather_id < 300:
        return "Heavy rainfall expected throughout the day"
    # Drizzle
    elif 300 <= weather_id < 400:
        return "Light drizzle expected intermittently"
    # Rain
    elif 500 <= weather_id < 600:
        if weather_id < 502:
            return "Light rainfall expected"
        else:
            return "Heavy rainfall expected"
    # Snow
    elif 600 <= weather_id < 700:
        return "Snowfall expected"
    # Atmosphere (fog, mist, etc.)
    elif 700 <= weather_id < 800:
        return "No rainfall expected, but humidity is high"
    # Clear
    elif weather_id == 800:
        return "No rainfall expected in the next 24 hours"
    # Clouds
    elif 801 <= weather_id < 900:
        if weather_id < 803:
            return "Low chance of rainfall"
        else:
            return "Moderate chance of rainfall"
    else:
        return "Weather conditions uncertain"

def get_farming_tip(weather_condition):
    """Generate farming tip based on weather condition"""
    if weather_condition == "Sunny":
        return "Good day for harvesting crops. Ensure proper hydration for plants."
    elif weather_condition == "Partly Cloudy":
        return "Moderate conditions for field work. Good time for planting."
    elif weather_condition == "Cloudy":
        return "Consider covering sensitive crops. Good time for planting."
    elif weather_condition == "Light Rain":
        return "Good day for planting. Avoid applying fertilizers."
    elif weather_condition == "Heavy Rain":
        return "Avoid field work. Ensure proper drainage in fields."
    elif weather_condition == "Snowy":
        return "Protect crops from frost. Avoid field work."
    else:
        return "Monitor weather conditions closely before undertaking field activities."

@climate_bp.route('/')
def climate_page():
    return render_template('climate.html')

@climate_bp.route('/api/climate/current', methods=['GET'])
def get_current_climate():
    try:
        region = request.args.get('region')
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        
        # If we have coordinates, use them to get real-time weather data
        if lat and lon and WEATHER_API_KEY:
            try:
                # Call OpenWeatherMap API
                weather_url = f"{WEATHER_API_URL}weather?lat={lat}&lon={lon}&units=metric&appid={WEATHER_API_KEY}"
                weather_response = requests.get(weather_url)
                weather_data = weather_response.json()
                
                if weather_response.status_code == 200:
                    # Map OpenWeatherMap weather conditions to our format
                    weather_id = weather_data['weather'][0]['id']
                    weather_condition = get_weather_condition(weather_id)
                    
                    # Get temperature
                    temperature = round(weather_data['main']['temp'], 1)
                    
                    # Get location name
                    location = weather_data['name']
                    
                    # Generate rainfall prediction based on weather
                    rainfall_prediction = get_rainfall_prediction(weather_id)
                    
                    # Generate farming tip based on weather
                    farming_tip = get_farming_tip(weather_condition)
                    
                    return jsonify({
                        'success': True,
                        'climate': {
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'temperature': temperature,
                            'weather_condition': weather_condition,
                            'rainfall_prediction': rainfall_prediction,
                            'farming_tip': farming_tip,
                            'region': location or region or 'Default'
                        },
                        'source': 'live_weather_api'
                    })
            except Exception as api_error:
                print(f"Weather API error: {str(api_error)}")
                # Fall back to database if API fails
                pass
        
        # Get the latest climate info from the database
        query = ClimateInfo.query.order_by(ClimateInfo.date.desc())
        
        if region:
            query = query.filter_by(region=region)
            
        climate = query.first()
        
        if not climate:
            # If no climate data exists, return hardcoded data
            return jsonify({
                'success': True,
                'climate': {
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'temperature': 28.5,
                    'weather_condition': 'Sunny',
                    'rainfall_prediction': 'No rainfall expected in the next 24 hours',
                    'farming_tip': 'Good day for harvesting crops. Ensure proper hydration for plants.',
                    'region': region or 'Default'
                },
                'note': 'Using default data as no climate information is available'
            })
            
        return jsonify({
            'success': True,
            'climate': {
                'date': climate.date.strftime('%Y-%m-%d'),
                'temperature': climate.temperature,
                'weather_condition': climate.weather_condition,
                'rainfall_prediction': climate.rainfall_prediction,
                'farming_tip': climate.farming_tip,
                'region': climate.region
            },
            'source': 'database'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@climate_bp.route('/api/climate/forecast', methods=['GET'])
def get_climate_forecast():
    try:
        region = request.args.get('region')
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        days = int(request.args.get('days', 5))
        
        # Limit days to a reasonable number
        if days > 10:
            days = 10
            
        # If we have coordinates and API key, use OpenWeatherMap API
        if lat and lon and WEATHER_API_KEY:
            try:
                # Call OpenWeatherMap 5-day forecast API
                forecast_url = f"{WEATHER_API_URL}forecast?lat={lat}&lon={lon}&units=metric&appid={WEATHER_API_KEY}"
                forecast_response = requests.get(forecast_url)
                forecast_data = forecast_response.json()
                
                if forecast_response.status_code == 200:
                    # Process the forecast data
                    processed_forecast = []
                    location = forecast_data['city']['name']
                    
                    # OpenWeatherMap returns forecast in 3-hour intervals
                    # We'll group by day and take the midday forecast for each day
                    forecasts_by_day = {}
                    
                    for item in forecast_data['list']:
                        dt = datetime.fromtimestamp(item['dt'])
                        date_str = dt.strftime('%Y-%m-%d')
                        
                        # If we don't have this day yet, or if this is closer to midday than what we have
                        hour = dt.hour
                        if date_str not in forecasts_by_day or abs(hour - 12) < abs(forecasts_by_day[date_str]['hour'] - 12):
                            weather_id = item['weather'][0]['id']
                            weather_condition = get_weather_condition(weather_id)
                            
                            forecasts_by_day[date_str] = {
                                'hour': hour,
                                'date': date_str,
                                'temperature': round(item['main']['temp'], 1),
                                'weather_condition': weather_condition,
                                'rainfall_prediction': get_rainfall_prediction(weather_id),
                                'farming_tip': get_farming_tip(weather_condition),
                                'region': location or region or 'Default'
                            }
                    
                    # Convert dictionary to list and sort by date
                    for date_str in sorted(forecasts_by_day.keys())[:days]:
                        processed_forecast.append(forecasts_by_day[date_str])
                    
                    return jsonify({
                        'success': True,
                        'forecast': processed_forecast,
                        'source': 'live_weather_api'
                    })
            except Exception as api_error:
                print(f"Weather API forecast error: {str(api_error)}")
                # Fall back to database if API fails
                pass
        
        # Get climate info for the next few days from database
        today = datetime.now().date()
        forecast_dates = [today + timedelta(days=i) for i in range(days)]
        
        # Query existing forecasts
        query = ClimateInfo.query.filter(ClimateInfo.date.in_(forecast_dates))
        
        if region:
            query = query.filter_by(region=region)
            
        existing_forecasts = query.all()
        
        # Create a dictionary of existing forecasts by date
        forecasts_by_date = {forecast.date: forecast for forecast in existing_forecasts}
        
        # Generate forecast data for each day
        forecast_data = []
        for date in forecast_dates:
            if date in forecasts_by_date:
                # Use existing forecast
                climate = forecasts_by_date[date]
                forecast_data.append({
                    'date': climate.date.strftime('%Y-%m-%d'),
                    'temperature': climate.temperature,
                    'weather_condition': climate.weather_condition,
                    'rainfall_prediction': climate.rainfall_prediction,
                    'farming_tip': climate.farming_tip,
                    'region': climate.region
                })
            else:
                # Generate mock forecast
                day_offset = (date - today).days
                weather_conditions = ['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Heavy Rain']
                weather_condition = weather_conditions[day_offset % len(weather_conditions)]
                
                temperature = 25 + (day_offset % 10) - 5
                
                if weather_condition == 'Sunny':
                    rainfall = 'No rainfall expected'
                    farming_tip = 'Good day for harvesting crops. Ensure proper hydration for plants.'
                elif weather_condition == 'Partly Cloudy':
                    rainfall = 'Low chance of light showers'
                    farming_tip = 'Moderate conditions for field work. Good time for planting.'
                elif weather_condition == 'Cloudy':
                    rainfall = 'Moderate chance of rainfall'
                    farming_tip = 'Consider covering sensitive crops. Good time for planting.'
                elif weather_condition == 'Light Rain':
                    rainfall = 'Light rainfall expected'
                    farming_tip = 'Good day for planting. Avoid applying fertilizers.'
                else:  # Heavy Rain
                    rainfall = 'Heavy rainfall expected'
                    farming_tip = 'Avoid field work. Ensure proper drainage in fields.'
                
                forecast_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'temperature': temperature,
                    'weather_condition': weather_condition,
                    'rainfall_prediction': rainfall,
                    'farming_tip': farming_tip,
                    'region': region or 'Default',
                    'note': 'Generated forecast'
                })
                
        return jsonify({
            'success': True,
            'forecast': forecast_data,
            'source': 'database'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@climate_bp.route('/api/climate/farming-tips', methods=['GET'])
def get_farming_tips():
    try:
        weather_condition = request.args.get('weather')
        
        # Define tips based on weather conditions
        tips = {
            'sunny': [
                'Ensure adequate irrigation for crops',
                'Apply mulch to retain soil moisture',
                'Best time for harvesting most crops',
                'Good time for drying harvested grains',
                'Consider shade for sensitive seedlings'
            ],
            'cloudy': [
                'Good conditions for transplanting seedlings',
                'Ideal for applying foliar fertilizers',
                'Reduced water needs for most crops',
                'Good time for field preparation',
                'Moderate conditions for most farm activities'
            ],
            'rainy': [
                'Avoid applying fertilizers that can wash away',
                'Check field drainage to prevent waterlogging',
                'Good time for planting most crops',
                'Delay harvesting if possible',
                'Watch for signs of fungal diseases in crops'
            ],
            'windy': [
                'Secure young plants and provide support',
                'Avoid spraying pesticides or herbicides',
                'Check for damage to crops and structures',
                'Delay transplanting seedlings if possible',
                'Ensure irrigation systems are working properly as soil may dry faster'
            ],
            'hot': [
                'Increase irrigation frequency',
                'Apply mulch to keep soil cool and retain moisture',
                'Provide shade for sensitive crops',
                'Avoid midday field operations',
                'Watch for signs of heat stress in plants'
            ],
            'cold': [
                'Cover sensitive crops to protect from frost',
                'Reduce irrigation frequency',
                'Delay sowing of warm-season crops',
                'Good time for pruning many trees',
                'Apply organic mulch to insulate soil'
            ]
        }
        
        # Default to general tips if no weather condition specified
        if not weather_condition or weather_condition.lower() not in tips:
            return jsonify({
                'success': True,
                'tips': [
                    'Regularly check soil moisture levels',
                    'Practice crop rotation to maintain soil health',
                    'Monitor crops for pest and disease signs',
                    'Use organic fertilizers when possible',
                    'Maintain proper spacing between plants',
                    'Keep records of planting dates and yields',
                    'Conserve water through efficient irrigation methods'
                ]
            })
            
        return jsonify({
            'success': True,
            'weather': weather_condition,
            'tips': tips[weather_condition.lower()]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500