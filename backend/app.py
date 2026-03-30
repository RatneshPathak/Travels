from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from config import Config
from models import db, User
import os

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Import routes
from routes import auth, user, admin, trips, activities

# Register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(user.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(trips.bp)
app.register_blueprint(activities.bp)

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Travel App API is running'}), 200

# Serve frontend - catch all routes for SPA
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return app.send_static_file(path)
    elif path.endswith('.html') and os.path.exists(os.path.join(app.static_folder, path)):
        return app.send_static_file(path)
    else:
        return app.send_static_file('index.html')

# Initialize database and seed admin
def init_db():
    """Initialize database and create admin user if not exists"""
    with app.app_context():
        # Create database directory if it doesn't exist
        db_dir = os.path.join(Config.BASE_DIR, 'database')
        os.makedirs(db_dir, exist_ok=True)
        
        # Create all tables
        db.create_all()
        
        # Create admin user if not exists
        admin = User.query.filter_by(email=Config.ADMIN_EMAIL).first()
        if not admin:
            admin = User(
                username=Config.ADMIN_USERNAME,
                email=Config.ADMIN_EMAIL,
                password_hash=bcrypt.generate_password_hash(Config.ADMIN_PASSWORD).decode('utf-8'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user created: {Config.ADMIN_EMAIL}")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8001, debug=True)