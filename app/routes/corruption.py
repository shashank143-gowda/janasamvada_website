from flask import Blueprint, request, jsonify, render_template, current_app
from app.models.models import db, CorruptionReport
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

corruption_bp = Blueprint('corruption_bp', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@corruption_bp.route('/')
def corruption_page():
    return render_template('corruption_redesigned_v3.html')

@corruption_bp.route('/report')
def report_corruption_page():
    return render_template('corruption_redesigned_v2.html')

@corruption_bp.route('/api/corruption/report', methods=['POST'])
def report_corruption():
    try:
        title = request.form.get('title')
        description = request.form.get('description')
        department = request.form.get('department')
        location = request.form.get('location')
        date_of_incident = request.form.get('date_of_incident')
        
        # Handle file upload
        evidence_path = None
        
        if 'evidence' in request.files:
            evidence = request.files['evidence']
            if evidence and allowed_file(evidence.filename):
                filename = secure_filename(f"{uuid.uuid4()}_{evidence.filename}")
                evidence_path = os.path.join('static/uploads', filename)
                evidence.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        
        # Parse date
        incident_date = datetime.strptime(date_of_incident, '%Y-%m-%d').date() if date_of_incident else datetime.now().date()
        
        new_report = CorruptionReport(
            title=title,
            description=description,
            department=department,
            location=location,
            date_of_incident=incident_date,
            evidence_path=evidence_path
        )
        
        db.session.add(new_report)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Corruption report submitted successfully',
            'report_id': new_report.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@corruption_bp.route('/api/corruption/status/<int:report_id>', methods=['GET'])
def check_status(report_id):
    try:
        report = CorruptionReport.query.get(report_id)
        
        if not report:
            return jsonify({
                'success': False,
                'error': 'Report not found'
            }), 404
            
        return jsonify({
            'success': True,
            'status': report.status,
            'created_at': report.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500