// Authentication logic

// Login form handler
if (document.getElementById('login-form')) {
    document.getElementById('login-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        clearError('error-message');
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        try {
            const data = await apiRequest('/auth/login', {
                method: 'POST',
                body: JSON.stringify({ email, password })
            });
            
            setToken(data.access_token);
            setUser(data.user);
            
            // Redirect based on role
            if (data.user.role === 'admin') {
                window.location.href = '/admin.html';
            } else {
                window.location.href = '/dashboard.html';
            }
        } catch (error) {
            showError('error-message', error.message);
        }
    });
}

// Register form handler
if (document.getElementById('register-form')) {
    document.getElementById('register-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        clearError('error-message');
        
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        try {
            const data = await apiRequest('/auth/register', {
                method: 'POST',
                body: JSON.stringify({ username, email, password })
            });
            
            setToken(data.access_token);
            setUser(data.user);
            
            window.location.href = '/dashboard.html';
        } catch (error) {
            showError('error-message', error.message);
        }
    });
}

// Logout handler
if (document.getElementById('logout-btn')) {
    document.getElementById('logout-btn').addEventListener('click', () => {
        removeToken();
        window.location.href = '/login.html';
    });
}