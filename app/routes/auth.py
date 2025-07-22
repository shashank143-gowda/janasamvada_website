from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from app.models.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            data = request.form
            
            # Check if user already exists
            existing_user = User.query.filter_by(username=data.get('username')).first()
            if existing_user:
                return jsonify({'success': False, 'message': 'Username already exists'}), 400
                
            existing_email = User.query.filter_by(email=data.get('email')).first()
            if existing_email:
                return jsonify({'success': False, 'message': 'Email already exists'}), 400
            
            # Create new user
            new_user = User(
                username=data.get('username'),
                email=data.get('email'),
                phone=data.get('phone'),
                village=data.get('village'),
                district=data.get('district'),
                state=data.get('state')
            )
            new_user.set_password(data.get('password'))
            
            db.session.add(new_user)
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Registration successful!'}), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            data = request.form
            
            # Find user by username
            user = User.query.filter_by(username=data.get('username')).first()
            
            if not user or not user.check_password(data.get('password')):
                return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
            
            # Set session
            session['user_id'] = user.id
            session['username'] = user.username
            
            return jsonify({
                'success': True, 
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'reward_points': user.reward_points
                }
            }), 200
            
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

@auth_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))
    
    return render_template('profile.html', user=user)

@auth_bp.route('/api/profile', methods=['GET'])
def get_profile():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
            'village': user.village,
            'district': user.district,
            'state': user.state,
            'reward_points': user.reward_points,
            'created_at': user.created_at.strftime('%Y-%m-%d')
        }
    })