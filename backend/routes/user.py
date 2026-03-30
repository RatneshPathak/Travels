from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Trip

bp = Blueprint('user', __name__, url_prefix='/api/user')

@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'username' in data:
            # Check if username is taken by another user
            existing = User.query.filter_by(username=data['username']).first()
            if existing and existing.id != user_id:
                return jsonify({'error': 'Username already taken'}), 400
            user.username = data['username']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Get user dashboard statistics"""
    try:
        user_id = get_jwt_identity()
        
        trips = Trip.query.filter_by(user_id=user_id).all()
        
        total_trips = len(trips)
        total_budget = sum(trip.total_budget for trip in trips)
        total_activities = sum(len(trip.activities) for trip in trips)
        
        return jsonify({
            'total_trips': total_trips,
            'total_budget': total_budget,
            'total_activities': total_activities,
            'recent_trips': [trip.to_dict() for trip in trips[:5]]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500