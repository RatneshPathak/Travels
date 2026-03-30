from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Trip, Activity
from functools import wraps

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def admin_required(fn):
    """Decorator to require admin role"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        return fn(*args, **kwargs)
    return wrapper


@bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    """Get all users (admin only)"""
    try:
        users = User.query.all()
        return jsonify({
            'users': [user.to_dict() for user in users],
            'total': len(users)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/trips', methods=['GET'])
@admin_required
def get_all_trips():
    """Get all trips (admin only)"""
    try:
        trips = Trip.query.all()
        return jsonify({
            'trips': [trip.to_dict() for trip in trips],
            'total': len(trips)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/analytics', methods=['GET'])
@admin_required
def get_analytics():
    """Get system analytics (admin only)"""
    try:
        total_users = User.query.count()
        total_trips = Trip.query.count()
        total_activities = Activity.query.count()
        
        # Calculate total budget across all trips
        trips = Trip.query.all()
        total_budget = sum(trip.total_budget for trip in trips)
        
        return jsonify({
            'total_users': total_users,
            'total_trips': total_trips,
            'total_activities': total_activities,
            'total_budget': total_budget
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Delete a user (admin only)"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.role == 'admin':
            return jsonify({'error': 'Cannot delete admin user'}), 403
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'User deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500