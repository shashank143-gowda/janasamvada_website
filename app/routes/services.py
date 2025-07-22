from flask import Blueprint, request, jsonify, render_template, session
from app.models.models import db, PublicService
import math

services_bp = Blueprint('services_bp', __name__)

@services_bp.route('/')
def services_page():
    return render_template('services_redesigned_v2.html', include_chatbot=True)
    
@services_bp.route('/classic')
def services_classic_page():
    return render_template('services.html')
    
@services_bp.route('/enhanced')
def services_enhanced_page():
    return render_template('services_enhanced.html')

@services_bp.route('/api/services', methods=['GET'])
def get_services():
    try:
        service_type = request.args.get('type')
        district = request.args.get('district')
        state = request.args.get('state')
        
        query = PublicService.query
        
        if service_type:
            query = query.filter_by(service_type=service_type)
        if district:
            query = query.filter_by(district=district)
        if state:
            query = query.filter_by(state=state)
            
        services = query.all()
        
        result = []
        for service in services:
            result.append({
                'id': service.id,
                'name': service.name,
                'type': service.service_type,
                'address': service.address,
                'contact': service.contact,
                'latitude': service.latitude,
                'longitude': service.longitude,
                'district': service.district,
                'state': service.state,
                'map_link': f"https://www.google.com/maps/search/?api=1&query={service.latitude},{service.longitude}"
            })
            
        return jsonify({
            'success': True,
            'services': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@services_bp.route('/api/services/nearby', methods=['GET'])
def get_nearby_services():
    try:
        # Get parameters from request
        lat = float(request.args.get('lat', 0))
        lng = float(request.args.get('lng', 0))
        radius = int(request.args.get('radius', 10))  # in kilometers
        service_type = request.args.get('type')
        
        # Log the request parameters for debugging
        print(f"API Request - lat: {lat}, lng: {lng}, radius: {radius}, type: {service_type}")
        
        if lat == 0 or lng == 0:
            return jsonify({
                'success': False,
                'error': 'Latitude and longitude are required'
            }), 400
            
        # Get all services
        query = PublicService.query
        if service_type and service_type.lower() != 'all':
            # Log the service type for debugging
            print(f"Filtering by service type: {service_type}")
            
            # Debug: Print all available service types in the database
            all_types = db.session.query(PublicService.service_type).distinct().all()
            print(f"Available service types in DB: {[t[0] for t in all_types]}")
            
            query = query.filter_by(service_type=service_type)
            
        all_services = query.all()
        
        # Calculate distance and filter by radius
        nearby_services = []
        for service in all_services:
            # Haversine formula to calculate distance
            dlat = math.radians(service.latitude - lat)
            dlng = math.radians(service.longitude - lng)
            a = math.sin(dlat/2)**2 + math.cos(math.radians(lat)) * math.cos(math.radians(service.latitude)) * math.sin(dlng/2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            distance = 6371 * c  # Earth radius in km
            
            if distance <= radius:
                nearby_services.append({
                    'id': service.id,
                    'name': service.name,
                    'type': service.service_type,
                    'address': service.address,
                    'contact': service.contact,
                    'latitude': service.latitude,
                    'longitude': service.longitude,
                    'district': service.district,
                    'state': service.state,
                    'distance': round(distance, 2),
                    'map_link': f"https://www.google.com/maps/search/?api=1&query={service.latitude},{service.longitude}"
                })
                
        # Sort by distance
        nearby_services.sort(key=lambda x: x['distance'])
        
        # Log the response for debugging
        print(f"API Response - Found {len(nearby_services)} services within {radius} km")
        
        return jsonify({
            'success': True,
            'services': nearby_services,
            'request_params': {
                'lat': lat,
                'lng': lng,
                'radius': radius,
                'type': service_type
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@services_bp.route('/api/services', methods=['POST'])
def add_service():
    # This would typically be an admin function
    try:
        data = request.json
        
        new_service = PublicService(
            name=data.get('name'),
            service_type=data.get('type'),
            address=data.get('address'),
            contact=data.get('contact'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            district=data.get('district'),
            state=data.get('state')
        )
        
        db.session.add(new_service)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Service added successfully',
            'service_id': new_service.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500