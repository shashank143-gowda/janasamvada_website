from flask import Blueprint, request, jsonify, render_template, session, current_app
from app.models.models import db, TreePlanting, User
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

trees_bp = Blueprint('trees_bp', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@trees_bp.route('/')
def trees_page():
    return render_template('trees.html')

@trees_bp.route('/plant')
def plant_tree_page():
    return render_template('plant_tree.html')

@trees_bp.route('/rewards')
def rewards_page():
    return render_template('rewards.html')

@trees_bp.route('/api/trees', methods=['GET'])
def get_trees():
    try:
        user_id = request.args.get('user_id')
        status = request.args.get('status')
        
        query = TreePlanting.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
            
        trees = query.order_by(TreePlanting.created_at.desc()).all()
        
        result = []
        for tree in trees:
            result.append({
                'id': tree.id,
                'user_id': tree.user_id,
                'username': tree.user.username if tree.user else 'Unknown',
                'tree_type': tree.tree_type,
                'image_path': tree.image_path,
                'latitude': tree.latitude,
                'longitude': tree.longitude,
                'location_description': tree.location_description,
                'status': tree.status,
                'points_awarded': tree.points_awarded,
                'created_at': tree.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'map_link': f"https://www.google.com/maps/search/?api=1&query={tree.latitude},{tree.longitude}" if tree.latitude and tree.longitude else None
            })
            
        return jsonify({
            'success': True,
            'trees': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@trees_bp.route('/api/trees', methods=['POST'])
def plant_tree():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login to plant a tree'}), 401
        
    try:
        tree_type = request.form.get('tree_type')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        location_description = request.form.get('location_description')
        
        # Handle image upload
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image provided'
            }), 400
            
        image = request.files['image']
        if not image or not allowed_file(image.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid image format'
            }), 400
            
        filename = secure_filename(f"{uuid.uuid4()}_{image.filename}")
        image_path = os.path.join('static/uploads', filename)
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        
        new_tree = TreePlanting(
            user_id=session['user_id'],
            tree_type=tree_type,
            image_path=image_path,
            latitude=float(latitude) if latitude else None,
            longitude=float(longitude) if longitude else None,
            location_description=location_description
        )
        
        db.session.add(new_tree)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tree planting recorded successfully',
            'tree_id': new_tree.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@trees_bp.route('/api/trees/<int:tree_id>/verify', methods=['POST'])
def verify_tree(tree_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login to verify a tree'}), 401
        
    try:
        # Check if user has admin privileges (simplified for demo)
        user = User.query.get(session['user_id'])
        if not user or user.id != 1:  # Assuming user with ID 1 is admin
            return jsonify({
                'success': False,
                'error': 'You do not have permission to verify trees'
            }), 403
            
        tree = TreePlanting.query.get(tree_id)
        
        if not tree:
            return jsonify({
                'success': False,
                'error': 'Tree planting record not found'
            }), 404
            
        # Update tree status and award points
        tree.status = 'verified'
        tree.points_awarded = 50  # Fixed points for now
        tree.verified_by = session['user_id']
        
        # Update user's reward points
        tree.user.reward_points += tree.points_awarded
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tree verified and points awarded',
            'points_awarded': tree.points_awarded,
            'user_total_points': tree.user.reward_points
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@trees_bp.route('/api/rewards/redeem', methods=['POST'])
def redeem_rewards():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login to redeem rewards'}), 401
        
    try:
        data = request.json
        points = int(data.get('points', 0))
        reward_type = data.get('reward_type')
        
        if points <= 0:
            return jsonify({
                'success': False,
                'error': 'Invalid points amount'
            }), 400
            
        if not reward_type:
            return jsonify({
                'success': False,
                'error': 'Reward type is required'
            }), 400
            
        user = User.query.get(session['user_id'])
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
            
        if user.reward_points < points:
            return jsonify({
                'success': False,
                'error': 'Insufficient points'
            }), 400
            
        # Create redemption record
        new_redemption = RewardRedemption(
            user_id=user.id,
            points_redeemed=points,
            reward_type=reward_type
        )
        
        # Deduct points from user
        user.reward_points -= points
        
        db.session.add(new_redemption)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Reward redemption successful',
            'redemption_id': new_redemption.id,
            'remaining_points': user.reward_points
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@trees_bp.route('/api/rewards/history', methods=['GET'])
def get_reward_history():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login to view reward history'}), 401
        
    try:
        user_id = session['user_id']
        
        # Get user's redemption history
        from app.models.models import RewardRedemption
        redemptions = RewardRedemption.query.filter_by(user_id=user_id).order_by(RewardRedemption.created_at.desc()).all()
        
        result = []
        for redemption in redemptions:
            result.append({
                'id': redemption.id,
                'points_redeemed': redemption.points_redeemed,
                'reward_type': redemption.reward_type,
                'status': redemption.status,
                'created_at': redemption.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
            
        return jsonify({
            'success': True,
            'redemptions': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500