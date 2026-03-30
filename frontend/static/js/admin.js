// Admin dashboard logic

if (!requireAuth()) {
    // Will redirect to login
} else {
    const user = getUser();
    if (user.role !== 'admin') {
        alert('Access denied. Admin privileges required.');
        window.location.href = '/dashboard.html';
    } else {
        loadAdminDashboard();
    }
}

async function loadAdminDashboard() {
    try {
        // Load analytics
        const analytics = await apiRequest('/admin/analytics');
        
        document.getElementById('total-users').textContent = analytics.total_users;
        document.getElementById('total-trips').textContent = analytics.total_trips;
        document.getElementById('total-activities').textContent = analytics.total_activities;
        document.getElementById('total-budget').textContent = formatCurrency(analytics.total_budget);
        
        // Load users
        loadAllUsers();
        
        // Load trips
        loadAllTrips();
        
    } catch (error) {
        console.error('Error loading admin dashboard:', error);
        if (error.message.includes('Admin access required')) {
            alert('Access denied. Admin privileges required.');
            window.location.href = '/dashboard.html';
        }
    }
}

async function loadAllUsers() {
    try {
        const data = await apiRequest('/admin/users');
        const usersList = document.getElementById('users-list');
        
        usersList.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Role</th>
                        <th>Created At</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.users.map(user => `
                        <tr data-testid="user-row-${user.id}">
                            <td>${user.id}</td>
                            <td>${user.username}</td>
                            <td>${user.email}</td>
                            <td>${user.role}</td>
                            <td>${formatDate(user.created_at)}</td>
                            <td>
                                ${user.role !== 'admin' ? `<button onclick="deleteUser(${user.id})" data-testid="delete-user-btn-${user.id}">Delete</button>` : '-'}
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        
    } catch (error) {
        console.error('Error loading users:', error);
    }
}

async function loadAllTrips() {
    try {
        const data = await apiRequest('/admin/trips');
        const tripsList = document.getElementById('trips-list');
        
        if (data.trips.length === 0) {
            tripsList.innerHTML = '<p>No trips in the system yet.</p>';
            return;
        }
        
        tripsList.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Title</th>
                        <th>Destination</th>
                        <th>User ID</th>
                        <th>Start Date</th>
                        <th>End Date</th>
                        <th>Budget</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.trips.map(trip => `
                        <tr data-testid="trip-row-${trip.id}">
                            <td>${trip.id}</td>
                            <td>${trip.title}</td>
                            <td>${trip.destination}</td>
                            <td>${trip.user_id}</td>
                            <td>${formatDate(trip.start_date)}</td>
                            <td>${formatDate(trip.end_date)}</td>
                            <td>${formatCurrency(trip.total_budget)}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        
    } catch (error) {
        console.error('Error loading trips:', error);
    }
}

async function deleteUser(userId) {
    if (!confirm('Are you sure you want to delete this user? This will also delete all their trips and activities.')) {
        return;
    }
    
    try {
        await apiRequest(`/admin/users/${userId}`, { method: 'DELETE' });
        loadAllUsers();
        loadAdminDashboard();
    } catch (error) {
        alert('Error deleting user: ' + error.message);
    }
}
