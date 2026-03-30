from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Trip, BudgetCategory
from datetime import datetime

bp = Blueprint('trips', __name__, url_prefix='/api/trips')

@bp.route('', methods=['GET'])
@jwt_required()
def get_trips():
    """Get all trips for current user"""
    try:
        user_id = get_jwt_identity()
        trips = Trip.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'trips': [trip.to_dict() for trip in trips],
            'total': len(trips)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:trip_id>', methods=['GET'])
@jwt_required()
def get_trip(trip_id):
    """Get a specific trip"""
    try:
        user_id = get_jwt_identity()
        trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
        
        if not trip:
            return jsonify({'error': 'Trip not found'}), 404
        
        return jsonify({'trip': trip.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('', methods=['POST'])
@jwt_required()
def create_trip():
    """Create a new trip"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['title', 'destination', 'start_date', 'end_date']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Parse dates
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        
        if end_date < start_date:
            return jsonify({'error': 'End date must be after start date'}), 400
        
        # Create trip
        new_trip = Trip(
            user_id=user_id,
            title=data['title'],
            destination=data['destination'],
            start_date=start_date,
            end_date=end_date,
            total_budget=data.get('total_budget', 0.0)
        )
        
        db.session.add(new_trip)
        db.session.commit()
        
        # Create default budget categories
        default_categories = ['Accommodation', 'Food', 'Transport', 'Activities', 'Other']
        for category in default_categories:
            budget_cat = BudgetCategory(
                trip_id=new_trip.id,
                category_name=category,
                allocated_amount=0.0,
                spent_amount=0.0
            )
            db.session.add(budget_cat)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Trip created successfully',
            'trip': new_trip.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:trip_id>', methods=['PUT'])
@jwt_required()
def update_trip(trip_id):
    """Update a trip"""
    try:
        user_id = get_jwt_identity()
        trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
        
        if not trip:
            return jsonify({'error': 'Trip not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'title' in data:
            trip.title = data['title']
        if 'destination' in data:
            trip.destination = data['destination']
        if 'start_date' in data:
            trip.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        if 'end_date' in data:
            trip.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        if 'total_budget' in data:
            trip.total_budget = data['total_budget']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Trip updated successfully',
            'trip': trip.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:trip_id>', methods=['DELETE'])
@jwt_required()
def delete_trip(trip_id):
    """Delete a trip"""
    try:
        user_id = get_jwt_identity()
        trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
        
        if not trip:
            return jsonify({'error': 'Trip not found'}), 404
        
        db.session.delete(trip)
        db.session.commit()
        
        return jsonify({'message': 'Trip deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:trip_id>/budget', methods=['PUT'])
@jwt_required()
def update_budget_category(trip_id):
    """Update budget category allocations"""
    try:
        user_id = get_jwt_identity()
        trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
        
        if not trip:
            return jsonify({'error': 'Trip not found'}), 404
        
        data = request.get_json()
        category_id = data.get('category_id')
        
        category = BudgetCategory.query.filter_by(id=category_id, trip_id=trip_id).first()
        
        if not category:
            return jsonify({'error': 'Budget category not found'}), 404
        
        if 'allocated_amount' in data:
            category.allocated_amount = data['allocated_amount']
        if 'spent_amount' in data:
            category.spent_amount = data['spent_amount']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Budget updated successfully',
            'category': category.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500