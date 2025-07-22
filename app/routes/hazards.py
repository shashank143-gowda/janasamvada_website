from flask import Blueprint, request, jsonify, render_template, session, current_app
from app.models.models import db, Hazard, User
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime
from app.utils.hazard_image_classifier import validate_hazard_image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

hazards_bp = Blueprint('hazards_bp', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@hazards_bp.route('/')
def hazards_page():
    return render_template('hazards_redesigned_v4.html', include_chatbot=True)

@hazards_bp.route('/report')
def report_hazard_page():
    return render_template('hazards_redesigned_v3.html', include_chatbot=True)

@hazards_bp.route('/api/validate-image', methods=['POST'])
def validate_image():
    """
    Validate if uploaded image is hazard-related using AI
    """
    try:
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No image file provided'
            }), 400
        
        image_file = request.files['image']
        
        if image_file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No image selected'
            }), 400
        
        if not allowed_file(image_file.filename):
            return jsonify({
                'success': False,
                'message': 'Invalid file type. Please upload JPG, PNG, or GIF images.'
            }), 400
        
        # Save temporary file for validation
        temp_filename = secure_filename(f"temp_{uuid.uuid4()}_{image_file.filename}")
        temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], temp_filename)
        image_file.save(temp_path)
        
        try:
            # Validate image using AI
            is_valid, confidence, hazard_type, message = validate_hazard_image(temp_path)
            
            logger.info(f"Image validation result: valid={is_valid}, confidence={confidence:.2f}%, type={hazard_type}")
            
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            if is_valid:
                return jsonify({
                    'success': True,
                    'is_hazard': True,
                    'confidence': round(confidence, 2),
                    'hazard_type': hazard_type,
                    'message': message
                })
            else:
                return jsonify({
                    'success': False,
                    'is_hazard': False,
                    'confidence': round(confidence, 2),
                    'message': "👉 Please upload a related picture."
                })
                
        except Exception as ai_error:
            # Clean up temporary file in case of error
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            logger.error(f"AI validation error: {str(ai_error)}")
            
            # Fall back to allowing upload if AI fails
            return jsonify({
                'success': True,
                'is_hazard': True,
                'confidence': 50.0,
                'hazard_type': 'unknown',
                'message': 'Image validation completed (AI temporarily unavailable)'
            })
            
    except Exception as e:
        logger.error(f"Error in image validation: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error validating image'
        }), 500

@hazards_bp.route('/api/hazards', methods=['GET'])
def get_hazards():
    try:
        hazard_type = request.args.get('type')
        status = request.args.get('status')
        
        query = Hazard.query
        
        if hazard_type:
            query = query.filter_by(hazard_type=hazard_type)
        if status:
            query = query.filter_by(status=status)
            
        # Order by upvotes and creation date
        hazards = query.order_by(Hazard.upvotes.desc(), Hazard.created_at.desc()).all()
        
        result = []
        for hazard in hazards:
            result.append({
                'id': hazard.id,
                'title': hazard.title,
                'description': hazard.description,
                'hazard_type': hazard.hazard_type,
                'image_path': hazard.image_path,
                'video_path': hazard.video_path,
                'latitude': hazard.latitude,
                'longitude': hazard.longitude,
                'location_description': hazard.location_description,
                'status': hazard.status,
                'upvotes': hazard.upvotes,
                'user_id': hazard.user_id,
                'username': hazard.user.username if hazard.user else 'Anonymous',
                'created_at': hazard.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'map_link': f"https://www.google.com/maps/search/?api=1&query={hazard.latitude},{hazard.longitude}" if hazard.latitude and hazard.longitude else None
            })
            
        return jsonify({
            'success': True,
            'hazards': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@hazards_bp.route('/api/hazards/<int:hazard_id>', methods=['GET'])
def get_hazard(hazard_id):
    try:
        hazard = Hazard.query.get(hazard_id)
        
        if not hazard:
            return jsonify({
                'success': False,
                'error': 'Hazard not found'
            }), 404
            
        return jsonify({
            'success': True,
            'hazard': {
                'id': hazard.id,
                'title': hazard.title,
                'description': hazard.description,
                'hazard_type': hazard.hazard_type,
                'image_path': hazard.image_path,
                'video_path': hazard.video_path,
                'latitude': hazard.latitude,
                'longitude': hazard.longitude,
                'location_description': hazard.location_description,
                'status': hazard.status,
                'upvotes': hazard.upvotes,
                'user_id': hazard.user_id,
                'username': hazard.user.username if hazard.user else 'Anonymous',
                'created_at': hazard.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'map_link': f"https://www.google.com/maps/search/?api=1&query={hazard.latitude},{hazard.longitude}" if hazard.latitude and hazard.longitude else None
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@hazards_bp.route('/api/hazards', methods=['POST'])
def report_hazard():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login to report a hazard'}), 401
        
    try:
        title = request.form.get('title')
        description = request.form.get('description')
        hazard_type = request.form.get('hazard_type')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        location_description = request.form.get('location_description')
        
        # Handle file uploads
        image_path = None
        video_path = None
        validation_results = []
        
        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                # Validate image using AI before saving
                temp_filename = secure_filename(f"temp_{uuid.uuid4()}_{image.filename}")
                temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], temp_filename)
                image.save(temp_path)
                
                try:
                    is_valid, confidence, hazard_type, message = validate_hazard_image(temp_path)
                    
                    if is_valid:
                        # If valid, save the image permanently
                        filename = secure_filename(f"{uuid.uuid4()}_{image.filename}")
                        image_path = os.path.join('static/uploads', filename)
                        final_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                        
                        # Move temp file to final location
                        os.rename(temp_path, final_path)
                        
                        validation_results.append({
                            'type': 'image',
                            'valid': True,
                            'confidence': confidence,
                            'hazard_type': hazard_type,
                            'message': message
                        })
                        
                        logger.info(f"Image validated and saved: {filename}, confidence: {confidence:.2f}%")
                    else:
                        # Remove temp file if invalid
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                        
                        return jsonify({
                            'success': False,
                            'message': '👉 Please upload a related picture.',
                            'validation_error': True,
                            'confidence': confidence
                        }), 400
                        
                except Exception as ai_error:
                    logger.error(f"AI validation error during upload: {str(ai_error)}")
                    # If AI fails, save the image anyway (fail-safe)
                    filename = secure_filename(f"{uuid.uuid4()}_{image.filename}")
                    image_path = os.path.join('static/uploads', filename)
                    final_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    
                    # Move temp file to final location
                    if os.path.exists(temp_path):
                        os.rename(temp_path, final_path)
                    
                    validation_results.append({
                        'type': 'image',
                        'valid': True,
                        'confidence': 50.0,
                        'hazard_type': 'unknown',
                        'message': 'Image uploaded (AI validation temporarily unavailable)'
                    })
                
        if 'video' in request.files:
            video = request.files['video']
            if video and allowed_file(video.filename):
                filename = secure_filename(f"{uuid.uuid4()}_{video.filename}")
                video_path = os.path.join('static/uploads', filename)
                video.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        
        new_hazard = Hazard(
            title=title,
            description=description,
            hazard_type=hazard_type,
            image_path=image_path,
            video_path=video_path,
            latitude=float(latitude) if latitude else None,
            longitude=float(longitude) if longitude else None,
            location_description=location_description,
            user_id=session['user_id']
        )
        
        db.session.add(new_hazard)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Hazard reported successfully',
            'hazard_id': new_hazard.id,
            'validation_results': validation_results
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@hazards_bp.route('/api/hazards/<int:hazard_id>/upvote', methods=['POST'])
def upvote_hazard(hazard_id):
    try:
        hazard = Hazard.query.get(hazard_id)
        
        if not hazard:
            return jsonify({
                'success': False,
                'error': 'Hazard not found'
            }), 404
            
        hazard.upvotes += 1
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Upvoted successfully',
            'upvotes': hazard.upvotes
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500