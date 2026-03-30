# Travel Planner Application

A comprehensive travel planning web application built with Flask (Python) backend and Vanilla JavaScript frontend.

## 🌟 Features

### User Module
- User registration and login with JWT authentication
- Personal dashboard with trip statistics
- Create, edit, and delete trips
- Budget tracking per trip
- Activity management with day-by-day itinerary
- Interactive maps with Leaflet.js
- Profile management

### Admin Module
- Admin dashboard with system analytics
- View all users and trips
- User management (delete non-admin users)
- System statistics (total users, trips, activities, budget)

### Travel Planner Module
- Multi-day itinerary builder
- Activity scheduling with time management
- Budget breakdown by categories (Accommodation, Food, Transport, Activities, Other)
- Interactive Leaflet.js maps with location markers
- Destination geocoding
- Cost tracking per activity

## 🛠️ Tech Stack

**Backend:**
- Python 3.11
- Flask 3.0.0
- SQLAlchemy (SQLite database)
- Flask-JWT-Extended (Authentication)
- Flask-Bcrypt (Password hashing)
- WeasyPrint (PDF export - ready for implementation)

**Frontend:**
- HTML5
- Vanilla JavaScript (ES6+)
- Water.css (Minimal CSS framework)
- Leaflet.js (Interactive maps)

## 📁 Project Structure

```
/app/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration
│   ├── models.py              # Database models
│   ├── requirements.txt       # Python dependencies
│   ├── routes/
│   │   ├── auth.py           # Authentication routes
│   │   ├── user.py           # User routes
│   │   ├── admin.py          # Admin routes
│   │   ├── trips.py          # Trip CRUD routes
│   │   └── activities.py     # Activity CRUD routes
│   └── database/
│       └── travel_app.db     # SQLite database
│
├── frontend/
│   ├── index.html            # Landing page
│   ├── login.html            # Login page
│   ├── register.html         # Registration page
│   ├── dashboard.html        # User dashboard
│   ├── trip-planner.html     # Trip planner with map
│   ├── admin.html            # Admin dashboard
│   ├── serve.py              # Static file server
│   └── static/
│       ├── css/
│       │   └── custom.css    # Custom styles
│       └── js/
│           ├── utils.js      # Utility functions
│           ├── auth.js       # Authentication logic
│           ├── dashboard.js  # Dashboard logic
│           ├── trip-planner.js # Trip planner logic
│           ├── map.js        # Leaflet map integration
│           └── admin.js      # Admin dashboard logic
```

## 🗄️ Database Schema

### Users Table
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- role (user/admin)
- created_at

### Trips Table
- id (Primary Key)
- user_id (Foreign Key)
- title
- destination
- start_date
- end_date
- total_budget
- created_at

### Activities Table
- id (Primary Key)
- trip_id (Foreign Key)
- title
- description
- day (Day number in trip)
- start_time
- end_time
- cost
- location
- latitude/longitude (for mapping)
- created_at

### Budget_Categories Table
- id (Primary Key)
- trip_id (Foreign Key)
- category_name
- allocated_amount
- spent_amount

## 🚀 Getting Started

### Installation

1. **Install Python dependencies:**
```bash
cd /app/backend
pip install -r requirements.txt
```

2. **Run the backend:**
```bash
cd /app/backend
python app.py
```

The backend will:
- Initialize the SQLite database
- Create an admin user automatically
- Run on `http://0.0.0.0:8001`

3. **Run the frontend:**
```bash
cd /app/frontend
python serve.py
```

The frontend will run on `http://0.0.0.0:3000`

### Default Credentials

**Admin Account:**
- Email: `admin@travelapp.com`
- Password: `Admin@123`

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### User
- `GET /api/user/profile` - Get user profile
- `PUT /api/user/profile` - Update user profile
- `GET /api/user/dashboard/stats` - Get dashboard statistics

### Trips
- `GET /api/trips` - Get all user trips
- `GET /api/trips/<id>` - Get specific trip
- `POST /api/trips` - Create new trip
- `PUT /api/trips/<id>` - Update trip
- `DELETE /api/trips/<id>` - Delete trip
- `PUT /api/trips/<id>/budget` - Update budget category

### Activities
- `GET /api/activities/trip/<trip_id>` - Get all activities for a trip
- `POST /api/activities` - Create new activity
- `PUT /api/activities/<id>` - Update activity
- `DELETE /api/activities/<id>` - Delete activity

### Admin (Requires admin role)
- `GET /api/admin/users` - Get all users
- `GET /api/admin/trips` - Get all trips
- `GET /api/admin/analytics` - Get system analytics
- `DELETE /api/admin/users/<id>` - Delete user

## 🗺️ Map Integration

The application uses Leaflet.js for interactive mapping:
- Displays destination location
- Shows activity locations with markers
- Uses OpenStreetMap tiles
- Geocoding via Nominatim API

## 🔒 Security Features

- JWT-based authentication
- Password hashing with Bcrypt
- Role-based access control (user/admin)
- CORS configuration
- SQL injection protection via SQLAlchemy ORM

## 📱 Features Overview

1. **User Registration & Login**
   - Secure authentication with JWT tokens
   - Password hashing
   - Persistent sessions

2. **Trip Management**
   - Create trips with destination, dates, and budget
   - View all your trips in one place
   - Edit or delete trips
   - Automatic budget category creation

3. **Itinerary Builder**
   - Add activities for each day of your trip
   - Set time slots for activities
   - Track costs per activity
   - Add location data for mapping

4. **Budget Tracking**
   - Categories: Accommodation, Food, Transport, Activities, Other
   - Track allocated vs spent amounts
   - View budget warnings and remaining balance

5. **Interactive Maps**
   - Visualize your trip destination
   - See all activity locations on a map
   - Click markers for activity details

6. **Admin Dashboard**
   - View all users and trips in the system
   - System-wide analytics
   - User management capabilities

## 🚧 Future Enhancements

- PDF export functionality (WeasyPrint already installed)
- Drag-and-drop itinerary reordering
- Multi-user trip collaboration
- Weather integration
- Photo uploads for activities
- Route planning with distance calculation
- Email notifications
- Mobile responsive design improvements
- PostgreSQL migration for production

## 📝 Development Notes

- The app uses SQLite for development (easy setup, no external dependencies)
- Ready for PostgreSQL migration (just update DATABASE_URL in config)
- Frontend served separately from backend for flexibility
- API-first design allows for future mobile app development
- Clean separation of concerns (routes, services, models)

## 🔧 Configuration

Environment variables can be set in `backend/config.py`:
- `JWT_SECRET_KEY` - Secret key for JWT tokens
- `DATABASE_URL` - Database connection string
- `ADMIN_EMAIL` - Default admin email
- `ADMIN_PASSWORD` - Default admin password

## 📄 License

This project is built as a demonstration of Flask + Vanilla JS architecture.

---

**Built with Flask 🌶️ and Vanilla JS 🍦**
