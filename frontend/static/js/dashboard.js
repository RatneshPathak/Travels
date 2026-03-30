// Dashboard logic

if (!requireAuth()) {
    // Will redirect to login
} else {
    // Load dashboard data
    loadDashboard();
}

async function loadDashboard() {
    const user = getUser();
    
    // Display user name
    document.getElementById('user-name').textContent = `Welcome, ${user.username}!`;
    
    // Show admin link if user is admin
    if (user.role === 'admin') {
        document.getElementById('admin-link').style.display = 'inline';
    }
    
    // Load stats
    try {
        const stats = await apiRequest('/user/dashboard/stats');
        
        document.getElementById('total-trips').textContent = stats.total_trips;
        document.getElementById('total-budget').textContent = formatCurrency(stats.total_budget);
        document.getElementById('total-activities').textContent = stats.total_activities;
        
        // Load trips
        loadTrips();
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

async function loadTrips() {
    try {
        const data = await apiRequest('/trips');
        const tripsList = document.getElementById('trips-list');
        
        if (data.trips.length === 0) {
            tripsList.innerHTML = '<p>No trips yet. Create your first trip!</p>';
            return;
        }
        
        tripsList.innerHTML = data.trips.map(trip => `
            <div class="trip-card" data-testid="trip-card-${trip.id}">
                <div class="trip-card-header">
                    <div>
                        <h3>${trip.title}</h3>
                        <p><strong>Destination:</strong> ${trip.destination}</p>
                        <p><strong>Dates:</strong> ${formatDate(trip.start_date)} - ${formatDate(trip.end_date)}</p>
                        <p><strong>Budget:</strong> ${formatCurrency(trip.total_budget)}</p>
                    </div>
                    <div class="trip-actions">
                        <button onclick="viewTrip(${trip.id})" data-testid="view-trip-btn-${trip.id}">View</button>
                        <button onclick="deleteTrip(${trip.id})" data-testid="delete-trip-btn-${trip.id}">Delete</button>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading trips:', error);
    }
}

function viewTrip(tripId) {
    window.location.href = `/trip-planner.html?trip=${tripId}`;
}

async function deleteTrip(tripId) {
    if (!confirm('Are you sure you want to delete this trip?')) {
        return;
    }
    
    try {
        await apiRequest(`/trips/${tripId}`, { method: 'DELETE' });
        loadTrips();
        loadDashboard();
    } catch (error) {
        alert('Error deleting trip: ' + error.message);
    }
}

// Create trip modal
const modal = document.getElementById('trip-modal');
const createBtn = document.getElementById('create-trip-btn');
const closeBtn = document.querySelector('.close');

createBtn.addEventListener('click', () => {
    modal.style.display = 'block';
});

closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
});

window.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.style.display = 'none';
    }
});

// Create trip form handler
document.getElementById('create-trip-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    clearError('modal-error');
    
    const title = document.getElementById('trip-title').value;
    const destination = document.getElementById('trip-destination').value;
    const start_date = document.getElementById('trip-start-date').value;
    const end_date = document.getElementById('trip-end-date').value;
    const total_budget = parseFloat(document.getElementById('trip-budget').value) || 0;
    
    try {
        await apiRequest('/trips', {
            method: 'POST',
            body: JSON.stringify({ title, destination, start_date, end_date, total_budget })
        });
        
        modal.style.display = 'none';
        document.getElementById('create-trip-form').reset();
        loadTrips();
        loadDashboard();
    } catch (error) {
        showError('modal-error', error.message);
    }
});