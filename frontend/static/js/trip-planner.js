// Trip planner logic with Leaflet map integration

if (!requireAuth()) {
    // Will redirect to login
} else {
    const urlParams = new URLSearchParams(window.location.search);
    const tripId = urlParams.get('trip');
    
    if (!tripId) {
        window.location.href = '/dashboard.html';
    } else {
        loadTripPlanner(tripId);
    }
}

let currentTrip = null;
let map = null;
let markers = [];

async function loadTripPlanner(tripId) {
    try {
        // Load trip details
        const tripData = await apiRequest(`/trips/${tripId}`);
        currentTrip = tripData.trip;
        
        // Display trip info
        document.getElementById('trip-title').textContent = currentTrip.title;
        document.getElementById('trip-destination').textContent = currentTrip.destination;
        
        const startDate = new Date(currentTrip.start_date);
        const endDate = new Date(currentTrip.end_date);
        const duration = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24)) + 1;
        document.getElementById('trip-duration').textContent = `${duration} days`;
        document.getElementById('trip-budget').textContent = currentTrip.total_budget.toFixed(2);
        
        // Load activities
        loadActivities(tripId);
        
        // Load budget categories
        loadBudgetCategories();
        
        // Initialize map
        initMap();
        
    } catch (error) {
        console.error('Error loading trip:', error);
        alert('Error loading trip details');
        window.location.href = '/dashboard.html';
    }
}

async function loadActivities(tripId) {
    try {
        const data = await apiRequest(`/activities/trip/${tripId}`);
        const activitiesList = document.getElementById('activities-list');
        
        if (data.activities.length === 0) {
            activitiesList.innerHTML = '<p>No activities yet. Add your first activity!</p>';
            return;
        }
        
        // Group activities by day
        const activitiesByDay = {};
        data.activities.forEach(activity => {
            if (!activitiesByDay[activity.day]) {
                activitiesByDay[activity.day] = [];
            }
            activitiesByDay[activity.day].push(activity);
        });
        
        let html = '';
        Object.keys(activitiesByDay).sort((a, b) => a - b).forEach(day => {
            html += `<h3>Day ${day}</h3>`;
            activitiesByDay[day].forEach(activity => {
                html += `
                    <div class="activity-item" data-testid="activity-item-${activity.id}">
                        <div class="activity-header">
                            <strong>${activity.title}</strong>
                            <button onclick="deleteActivity(${activity.id})" data-testid="delete-activity-btn-${activity.id}">Delete</button>
                        </div>
                        <p>${activity.description || ''}</p>
                        ${activity.start_time ? `<p><strong>Time:</strong> ${activity.start_time} - ${activity.end_time}</p>` : ''}
                        ${activity.location ? `<p><strong>Location:</strong> ${activity.location}</p>` : ''}
                        <p><strong>Cost:</strong> $${activity.cost.toFixed(2)}</p>
                    </div>
                `;
            });
        });
        
        activitiesList.innerHTML = html;
        
        // Update map markers
        updateMapMarkers(data.activities);
        
    } catch (error) {
        console.error('Error loading activities:', error);
    }
}

function loadBudgetCategories() {
    const budgetCategories = document.getElementById('budget-categories');
    
    if (!currentTrip.budget_categories || currentTrip.budget_categories.length === 0) {
        budgetCategories.innerHTML = '<p>No budget categories available.</p>';
        return;
    }
    
    budgetCategories.innerHTML = currentTrip.budget_categories.map(cat => `
        <div class="budget-category" data-testid="budget-category-${cat.id}">
            <strong>${cat.category_name}</strong>
            <p>Allocated: $${cat.allocated_amount.toFixed(2)}</p>
            <p>Spent: $${cat.spent_amount.toFixed(2)}</p>
            <p>Remaining: $${cat.remaining.toFixed(2)}</p>
        </div>
    `).join('');
}

async function deleteActivity(activityId) {
    if (!confirm('Are you sure you want to delete this activity?')) {
        return;
    }
    
    try {
        await apiRequest(`/activities/${activityId}`, { method: 'DELETE' });
        loadActivities(currentTrip.id);
    } catch (error) {
        alert('Error deleting activity: ' + error.message);
    }
}

// Back to dashboard
document.getElementById('back-btn').addEventListener('click', () => {
    window.location.href = '/dashboard.html';
});

// Add activity modal
const activityModal = document.getElementById('activity-modal');
const addActivityBtn = document.getElementById('add-activity-btn');
const closeActivityModal = document.querySelector('#activity-modal .close');

addActivityBtn.addEventListener('click', () => {
    activityModal.style.display = 'block';
});

closeActivityModal.addEventListener('click', () => {
    activityModal.style.display = 'none';
});

window.addEventListener('click', (e) => {
    if (e.target === activityModal) {
        activityModal.style.display = 'none';
    }
});

// Add activity form handler
document.getElementById('add-activity-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    clearError('activity-modal-error');
    
    const title = document.getElementById('activity-title').value;
    const description = document.getElementById('activity-description').value;
    const day = parseInt(document.getElementById('activity-day').value);
    const start_time = document.getElementById('activity-start-time').value;
    const end_time = document.getElementById('activity-end-time').value;
    const cost = parseFloat(document.getElementById('activity-cost').value) || 0;
    const location = document.getElementById('activity-location').value;
    
    try {
        await apiRequest('/activities', {
            method: 'POST',
            body: JSON.stringify({
                trip_id: currentTrip.id,
                title,
                description,
                day,
                start_time,
                end_time,
                cost,
                location
            })
        });
        
        activityModal.style.display = 'none';
        document.getElementById('add-activity-form').reset();
        loadActivities(currentTrip.id);
    } catch (error) {
        showError('activity-modal-error', error.message);
    }
});