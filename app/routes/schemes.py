from flask import Blueprint, request, jsonify, render_template
from app.models.models import db, GovernmentScheme

schemes_bp = Blueprint('schemes_bp', __name__)

@schemes_bp.route('/')
def schemes_page():
    return render_template('schemes_redesigned_v2.html', include_chatbot=True)

@schemes_bp.route('/api/schemes', methods=['GET'])
def get_schemes():
    try:
        category = request.args.get('category')
        
        query = GovernmentScheme.query
        
        if category:
            query = query.filter_by(category=category)
            
        schemes = query.all()
        
        result = []
        for scheme in schemes:
            result.append({
                'id': scheme.id,
                'name': scheme.name,
                'category': scheme.category,
                'description': scheme.description,
                'eligibility': scheme.eligibility,
                'application_process': scheme.application_process,
                'documents_required': scheme.documents_required,
                'contact_info': scheme.contact_info,
                'website': scheme.website
            })
            
        return jsonify({
            'success': True,
            'schemes': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@schemes_bp.route('/api/schemes/<int:scheme_id>', methods=['GET'])
def get_scheme(scheme_id):
    try:
        scheme = GovernmentScheme.query.get(scheme_id)
        
        if not scheme:
            return jsonify({
                'success': False,
                'error': 'Scheme not found'
            }), 404
            
        return jsonify({
            'success': True,
            'scheme': {
                'id': scheme.id,
                'name': scheme.name,
                'category': scheme.category,
                'description': scheme.description,
                'eligibility': scheme.eligibility,
                'application_process': scheme.application_process,
                'documents_required': scheme.documents_required,
                'contact_info': scheme.contact_info,
                'website': scheme.website
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@schemes_bp.route('/api/schemes/categories', methods=['GET'])
def get_categories():
    try:
        # Get distinct categories
        categories = db.session.query(GovernmentScheme.category).distinct().all()
        
        return jsonify({
            'success': True,
            'categories': [category[0] for category in categories]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@schemes_bp.route('/api/schemes', methods=['POST'])
def add_scheme():
    # This would typically be an admin function
    try:
        data = request.json
        
        new_scheme = GovernmentScheme(
            name=data.get('name'),
            category=data.get('category'),
            description=data.get('description'),
            eligibility=data.get('eligibility'),
            application_process=data.get('application_process'),
            documents_required=data.get('documents_required'),
            contact_info=data.get('contact_info'),
            website=data.get('website')
        )
        
        db.session.add(new_scheme)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Scheme added successfully',
            'scheme_id': new_scheme.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500