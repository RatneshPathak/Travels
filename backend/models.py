from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication and profile"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    trips = db.relationship('Trip', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }


class Trip(db.Model):
    """Trip model for travel planning"""
    __tablename__ = 'trips'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    destination = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_budget = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    activities = db.relationship('Activity', backref='trip', lazy=True, cascade='all, delete-orphan')
    budget_categories = db.relationship('BudgetCategory', backref='trip', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'destination': self.destination,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'total_budget': self.total_budget,
            'created_at': self.created_at.isoformat(),
            'activities': [activity.to_dict() for activity in self.activities],
            'budget_categories': [cat.to_dict() for cat in self.budget_categories]
        }


class Activity(db.Model):
    """Activity model for itinerary items"""
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    day = db.Column(db.Integer, nullable=False)  # Day number in the trip
    start_time = db.Column(db.String(10))  # Format: HH:MM
    end_time = db.Column(db.String(10))    # Format: HH:MM
    cost = db.Column(db.Float, default=0.0)
    location = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'trip_id': self.trip_id,
            'title': self.title,
            'description': self.description,
            'day': self.day,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'cost': self.cost,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'created_at': self.created_at.isoformat()
        }


class BudgetCategory(db.Model):
    """Budget category model for expense tracking"""
    __tablename__ = 'budget_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    category_name = db.Column(db.String(100), nullable=False)  # e.g., 'Food', 'Transport', 'Accommodation'
    allocated_amount = db.Column(db.Float, default=0.0)
    spent_amount = db.Column(db.Float, default=0.0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'trip_id': self.trip_id,
            'category_name': self.category_name,
            'allocated_amount': self.allocated_amount,
            'spent_amount': self.spent_amount,
            'remaining': self.allocated_amount - self.spent_amount
        }