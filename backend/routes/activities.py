from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Trip, Activity

bp = Blueprint('activities', __name__, url_prefix='/api/activities')

@bp.route('/trip/<int:trip_id>', methods=['GET'])
@jwt_required()
def get_activities(trip_id):
    """Get all activities for a trip"""
    try:
        user_id = get_jwt_identity()
        trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
        
        if not trip:
            return jsonify({'error': 'Trip not found'}), 404
        
        activities = Activity.query.filter_by(trip_id=trip_id).order_by(Activity.day, Activity.start_time).all()
        
        return jsonify({
            'activities': [activity.to_dict() for activity in activities],
            'total': len(activities)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('', methods=['POST'])
@jwt_required()
def create_activity():
    """Create a new activity"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate trip ownership
        trip = Trip.query.filter_by(id=data.get('trip_id'), user_id=user_id).first()
        if not trip:
            return jsonify({'error': 'Trip not found'}), 404
        
        # Create activity
        new_activity = Activity(
            trip_id=data['trip_id'],
            title=data['title'],
            description=data.get('description', ''),
            day=data['day'],
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            cost=data.get('cost', 0.0),
            location=data.get('location'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude')
        )
        
        db.session.add(new_activity)
        db.session.commit()
        
        return jsonify({
            'message': 'Activity created successfully',
            'activity': new_activity.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:activity_id>', methods=['PUT'])
@jwt_required()
def update_activity(activity_id):
    """Update an activity"""
    try:
        user_id = get_jwt_identity()
        activity = Activity.query.get(activity_id)
        
        if not activity:
            return jsonify({'error': 'Activity not found'}), 404
        
        # Verify trip ownership
        trip = Trip.query.filter_by(id=activity.trip_id, user_id=user_id).first()
        if not trip:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        # Update fields
        if 'title' in data:
            activity.title = data['title']
        if 'description' in data:
            activity.description = data['description']
        if 'day' in data:
            activity.day = data['day']
        if 'start_time' in data:
            activity.start_time = data['start_time']
        if 'end_time' in data:
            activity.end_time = data['end_time']
        if 'cost' in data:
            activity.cost = data['cost']
        if 'location' in data:
            activity.location = data['location']
        if 'latitude' in data:
            activity.latitude = data['latitude']
        if 'longitude' in data:
            activity.longitude = data['longitude']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Activity updated successfully',
            'activity': activity.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:activity_id>', methods=['DELETE'])
@jwt_required()
def delete_activity(activity_id):
    """Delete an activity"""
    try:
        user_id = get_jwt_identity()
        activity = Activity.query.get(activity_id)
        
        if not activity:
            return jsonify({'error': 'Activity not found'}), 404
        
        # Verify trip ownership
        trip = Trip.query.filter_by(id=activity.trip_id, user_id=user_id).first()
        if not trip:
            return jsonify({'error': 'Unauthorized'}), 403
        
        db.session.delete(activity)
        db.session.commit()
        
        return jsonify({'message': 'Activity deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500