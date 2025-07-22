from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session, current_app
from app.models.models import db, User, Hazard, PublicService, GovernmentScheme, CorruptionReport, TreePlanting, ClimateInfo, RewardRedemption
from functools import wraps
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename
import uuid
import json

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'danger')
            return redirect(url_for('admin.login'))
        
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            flash('You do not have permission to access this page', 'danger')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function

# Admin Login
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            data = request.form
            
            # Find user by username
            user = User.query.filter_by(username=data.get('username')).first()
            
            if not user or not user.check_password(data.get('password')) or user.role != 'admin':
                return jsonify({'success': False, 'message': 'Invalid username or password, or you do not have admin privileges'}), 401
            
            # Set session
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = True
            
            # Update last login time
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                'success': True, 
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }), 200
            
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    return render_template('admin/login.html')

# Dashboard
@admin_bp.route('/')
@admin_required
def dashboard():
    # Get statistics
    stats = {
        'users': User.query.count(),
        'resolved_hazards': Hazard.query.filter_by(status='resolved').count(),
        'trees_planted': TreePlanting.query.filter_by(status='verified').count(),
        'pending_reports': Hazard.query.filter_by(status='pending').count() + CorruptionReport.query.filter_by(status='under review').count()
    }
    
    # Get recent hazards
    recent_hazards = Hazard.query.order_by(Hazard.created_at.desc()).limit(5).all()
    
    # Get recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    # Prepare chart data
    chart_data = {
        'hazards': {
            'labels': [],
            'data': []
        },
        'hazard_types': []
    }
    
    # Last 7 days hazards
    for i in range(7, 0, -1):
        date = datetime.now() - timedelta(days=i-1)
        date_str = date.strftime('%Y-%m-%d')
        chart_data['hazards']['labels'].append(date_str)
        
        count = Hazard.query.filter(
            db.func.date(Hazard.created_at) == date.date()
        ).count()
        
        chart_data['hazards']['data'].append(count)
    
    # Hazard types distribution
    road_count = Hazard.query.filter_by(hazard_type='road').count()
    water_count = Hazard.query.filter_by(hazard_type='water').count()
    electricity_count = Hazard.query.filter_by(hazard_type='electricity').count()
    other_count = Hazard.query.filter_by(hazard_type='other').count()
    
    chart_data['hazard_types'] = [road_count, water_count, electricity_count, other_count]
    
    # Get current user's last login time
    user = User.query.get(session['user_id'])
    if user and user.last_login:
        session['last_login'] = user.last_login.strftime('%d %b, %Y at %H:%M')
    
    return render_template('admin/dashboard.html', 
                          stats=stats, 
                          recent_hazards=recent_hazards, 
                          recent_users=recent_users, 
                          chart_data=chart_data,
                          now=datetime.now())

# Users management
@admin_bp.route('/users')
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    users = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page)
    
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.phone = request.form.get('phone')
        user.village = request.form.get('village')
        user.district = request.form.get('district')
        user.state = request.form.get('state')
        user.reward_points = request.form.get('reward_points', type=int)
        
        if request.form.get('password'):
            user.set_password(request.form.get('password'))
        
        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/edit_user.html', user=user)

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Delete related records
    Hazard.query.filter_by(user_id=user_id).delete()
    TreePlanting.query.filter_by(user_id=user_id).delete()
    RewardRedemption.query.filter_by(user_id=user_id).delete()
    
    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully', 'success')
    return redirect(url_for('admin.users'))

# Hazards management
@admin_bp.route('/hazards')
@admin_required
def hazards():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    hazards = Hazard.query.order_by(Hazard.created_at.desc()).paginate(page=page, per_page=per_page)
    
    return render_template('admin/hazards.html', hazards=hazards)

@admin_bp.route('/hazards/<int:hazard_id>', methods=['GET', 'POST'])
@admin_required
def edit_hazard(hazard_id):
    hazard = Hazard.query.get_or_404(hazard_id)
    
    if request.method == 'POST':
        hazard.title = request.form.get('title')
        hazard.description = request.form.get('description')
        hazard.hazard_type = request.form.get('hazard_type')
        hazard.status = request.form.get('status')
        hazard.location_description = request.form.get('location_description')
        
        if 'image' in request.files and request.files['image'].filename:
            image = request.files['image']
            if image and allowed_file(image.filename):
                # Delete old image if exists
                if hazard.image_path and os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], hazard.image_path)):
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], hazard.image_path))
                
                filename = secure_filename(f"{uuid.uuid4()}_{image.filename}")
                image_path = os.path.join('static/uploads', filename)
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                hazard.image_path = image_path
        
        db.session.commit()
        flash('Hazard updated successfully', 'success')
        return redirect(url_for('admin.hazards'))
    
    return render_template('admin/edit_hazard.html', hazard=hazard)

@admin_bp.route('/hazards/<int:hazard_id>/delete', methods=['POST'])
@admin_required
def delete_hazard(hazard_id):
    hazard = Hazard.query.get_or_404(hazard_id)
    
    # Delete image if exists
    if hazard.image_path and os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], hazard.image_path)):
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], hazard.image_path))
    
    # Delete video if exists
    if hazard.video_path and os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], hazard.video_path)):
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], hazard.video_path))
    
    db.session.delete(hazard)
    db.session.commit()
    
    flash('Hazard deleted successfully', 'success')
    return redirect(url_for('admin.hazards'))

# Services management
@admin_bp.route('/services')
@admin_required
def services():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    services = PublicService.query.order_by(PublicService.name).paginate(page=page, per_page=per_page)
    
    return render_template('admin/services.html', services=services)

@admin_bp.route('/services/new', methods=['GET', 'POST'])
@admin_required
def new_service():
    if request.method == 'POST':
        service = PublicService(
            name=request.form.get('name'),
            service_type=request.form.get('service_type'),
            address=request.form.get('address'),
            contact=request.form.get('contact'),
            latitude=float(request.form.get('latitude')) if request.form.get('latitude') else None,
            longitude=float(request.form.get('longitude')) if request.form.get('longitude') else None,
            district=request.form.get('district'),
            state=request.form.get('state')
        )
        
        db.session.add(service)
        db.session.commit()
        
        flash('Service added successfully', 'success')
        return redirect(url_for('admin.services'))
    
    return render_template('admin/edit_service.html')

@admin_bp.route('/services/<int:service_id>', methods=['GET', 'POST'])
@admin_required
def edit_service(service_id):
    service = PublicService.query.get_or_404(service_id)
    
    if request.method == 'POST':
        service.name = request.form.get('name')
        service.service_type = request.form.get('service_type')
        service.address = request.form.get('address')
        service.contact = request.form.get('contact')
        service.latitude = float(request.form.get('latitude')) if request.form.get('latitude') else None
        service.longitude = float(request.form.get('longitude')) if request.form.get('longitude') else None
        service.district = request.form.get('district')
        service.state = request.form.get('state')
        
        db.session.commit()
        flash('Service updated successfully', 'success')
        return redirect(url_for('admin.services'))
    
    return render_template('admin/edit_service.html', service=service)

@admin_bp.route('/services/<int:service_id>/delete', methods=['POST'])
@admin_required
def delete_service(service_id):
    service = PublicService.query.get_or_404(service_id)
    
    db.session.delete(service)
    db.session.commit()
    
    flash('Service deleted successfully', 'success')
    return redirect(url_for('admin.services'))

# Schemes management
@admin_bp.route('/schemes')
@admin_required
def schemes():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    schemes = GovernmentScheme.query.order_by(GovernmentScheme.name).paginate(page=page, per_page=per_page)
    
    return render_template('admin/schemes.html', schemes=schemes)

@admin_bp.route('/schemes/new', methods=['GET', 'POST'])
@admin_required
def new_scheme():
    if request.method == 'POST':
        scheme = GovernmentScheme(
            name=request.form.get('name'),
            category=request.form.get('category'),
            description=request.form.get('description'),
            eligibility=request.form.get('eligibility'),
            application_process=request.form.get('application_process'),
            documents_required=request.form.get('documents_required'),
            contact_info=request.form.get('contact_info'),
            website=request.form.get('website')
        )
        
        db.session.add(scheme)
        db.session.commit()
        
        flash('Scheme added successfully', 'success')
        return redirect(url_for('admin.schemes'))
    
    return render_template('admin/edit_scheme.html')

@admin_bp.route('/schemes/<int:scheme_id>', methods=['GET', 'POST'])
@admin_required
def edit_scheme(scheme_id):
    scheme = GovernmentScheme.query.get_or_404(scheme_id)
    
    if request.method == 'POST':
        scheme.name = request.form.get('name')
        scheme.category = request.form.get('category')
        scheme.description = request.form.get('description')
        scheme.eligibility = request.form.get('eligibility')
        scheme.application_process = request.form.get('application_process')
        scheme.documents_required = request.form.get('documents_required')
        scheme.contact_info = request.form.get('contact_info')
        scheme.website = request.form.get('website')
        
        db.session.commit()
        flash('Scheme updated successfully', 'success')
        return redirect(url_for('admin.schemes'))
    
    return render_template('admin/edit_scheme.html', scheme=scheme)

@admin_bp.route('/schemes/<int:scheme_id>/delete', methods=['POST'])
@admin_required
def delete_scheme(scheme_id):
    scheme = GovernmentScheme.query.get_or_404(scheme_id)
    
    db.session.delete(scheme)
    db.session.commit()
    
    flash('Scheme deleted successfully', 'success')
    return redirect(url_for('admin.schemes'))

# Corruption reports management
@admin_bp.route('/corruption')
@admin_required
def corruption():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    reports = CorruptionReport.query.order_by(CorruptionReport.created_at.desc()).paginate(page=page, per_page=per_page)
    
    return render_template('admin/corruption.html', reports=reports)

@admin_bp.route('/corruption/<int:report_id>', methods=['GET', 'POST'])
@admin_required
def edit_corruption(report_id):
    report = CorruptionReport.query.get_or_404(report_id)
    
    if request.method == 'POST':
        report.title = request.form.get('title')
        report.description = request.form.get('description')
        report.department = request.form.get('department')
        report.location = request.form.get('location')
        report.status = request.form.get('status')
        
        db.session.commit()
        flash('Report updated successfully', 'success')
        return redirect(url_for('admin.corruption'))
    
    return render_template('admin/edit_corruption.html', report=report)

@admin_bp.route('/corruption/<int:report_id>/delete', methods=['POST'])
@admin_required
def delete_corruption(report_id):
    report = CorruptionReport.query.get_or_404(report_id)
    
    # Delete evidence if exists
    if report.evidence_path and os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], report.evidence_path)):
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], report.evidence_path))
    
    db.session.delete(report)
    db.session.commit()
    
    flash('Report deleted successfully', 'success')
    return redirect(url_for('admin.corruption'))

# Tree plantings management
@admin_bp.route('/trees')
@admin_required
def trees():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    trees = TreePlanting.query.order_by(TreePlanting.created_at.desc()).paginate(page=page, per_page=per_page)
    
    return render_template('admin/trees.html', trees=trees)

@admin_bp.route('/trees/<int:tree_id>', methods=['GET', 'POST'])
@admin_required
def edit_tree(tree_id):
    tree = TreePlanting.query.get_or_404(tree_id)
    
    if request.method == 'POST':
        tree.tree_type = request.form.get('tree_type')
        tree.location_description = request.form.get('location_description')
        tree.status = request.form.get('status')
        
        # If status changed to verified, update points
        if tree.status == 'verified' and request.form.get('status') == 'verified' and tree.points_awarded == 0:
            tree.points_awarded = 10  # Default points for planting a tree
            tree.verified_by = session['user_id']
            
            # Update user's reward points
            user = User.query.get(tree.user_id)
            if user:
                user.reward_points += tree.points_awarded
        
        db.session.commit()
        flash('Tree planting record updated successfully', 'success')
        return redirect(url_for('admin.trees'))
    
    return render_template('admin/edit_tree.html', tree=tree)

@admin_bp.route('/trees/<int:tree_id>/delete', methods=['POST'])
@admin_required
def delete_tree(tree_id):
    tree = TreePlanting.query.get_or_404(tree_id)
    
    # Delete image if exists
    if tree.image_path and os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], tree.image_path)):
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], tree.image_path))
    
    # If tree was verified, remove points from user
    if tree.status == 'verified' and tree.points_awarded > 0:
        user = User.query.get(tree.user_id)
        if user:
            user.reward_points -= tree.points_awarded
    
    db.session.delete(tree)
    db.session.commit()
    
    flash('Tree planting record deleted successfully', 'success')
    return redirect(url_for('admin.trees'))

# Climate info management
@admin_bp.route('/climate')
@admin_required
def climate():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    climate_info = ClimateInfo.query.order_by(ClimateInfo.date.desc()).paginate(page=page, per_page=per_page)
    
    return render_template('admin/climate.html', climate_info=climate_info)

@admin_bp.route('/climate/new', methods=['GET', 'POST'])
@admin_required
def new_climate():
    if request.method == 'POST':
        climate = ClimateInfo(
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date(),
            temperature=float(request.form.get('temperature')) if request.form.get('temperature') else None,
            weather_condition=request.form.get('weather_condition'),
            rainfall_prediction=request.form.get('rainfall_prediction'),
            farming_tip=request.form.get('farming_tip'),
            region=request.form.get('region')
        )
        
        db.session.add(climate)
        db.session.commit()
        
        flash('Climate information added successfully', 'success')
        return redirect(url_for('admin.climate'))
    
    return render_template('admin/edit_climate.html')

@admin_bp.route('/climate/<int:climate_id>', methods=['GET', 'POST'])
@admin_required
def edit_climate(climate_id):
    climate = ClimateInfo.query.get_or_404(climate_id)
    
    if request.method == 'POST':
        climate.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        climate.temperature = float(request.form.get('temperature')) if request.form.get('temperature') else None
        climate.weather_condition = request.form.get('weather_condition')
        climate.rainfall_prediction = request.form.get('rainfall_prediction')
        climate.farming_tip = request.form.get('farming_tip')
        climate.region = request.form.get('region')
        
        db.session.commit()
        flash('Climate information updated successfully', 'success')
        return redirect(url_for('admin.climate'))
    
    return render_template('admin/edit_climate.html', climate=climate)

@admin_bp.route('/climate/<int:climate_id>/delete', methods=['POST'])
@admin_required
def delete_climate(climate_id):
    climate = ClimateInfo.query.get_or_404(climate_id)
    
    db.session.delete(climate)
    db.session.commit()
    
    flash('Climate information deleted successfully', 'success')
    return redirect(url_for('admin.climate'))

# News management
@admin_bp.route('/news')
@admin_required
def news():
    # This would typically fetch from a News model
    # For now, we'll use a placeholder
    return render_template('admin/news.html')

# Settings
@admin_bp.route('/settings', methods=['GET', 'POST'])
@admin_required
def settings():
    if request.method == 'POST':
        # Update application settings
        # This would typically update a Settings model or configuration file
        flash('Settings updated successfully', 'success')
        return redirect(url_for('admin.settings'))
    
    return render_template('admin/settings.html')

# Helper function for file uploads
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']