// Map integration with Leaflet.js

function initMap() {
    // Initialize map centered on world view
    map = L.map('map').setView([20, 0], 2);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }).addTo(map);
    
    // Try to geocode the destination and center the map
    if (currentTrip && currentTrip.destination) {
        geocodeDestination(currentTrip.destination);
    }
}

function updateMapMarkers(activities) {
    // Clear existing markers
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];
    
    // Add markers for activities with coordinates
    activities.forEach(activity => {
        if (activity.latitude && activity.longitude) {
            const marker = L.marker([activity.latitude, activity.longitude])
                .addTo(map)
                .bindPopup(`
                    <strong>${activity.title}</strong><br>
                    ${activity.location || ''}<br>
                    Day ${activity.day}<br>
                    Cost: $${activity.cost.toFixed(2)}
                `);
            markers.push(marker);
        }
    });
    
    // Fit map to show all markers
    if (markers.length > 0) {
        const group = L.featureGroup(markers);
        map.fitBounds(group.getBounds().pad(0.1));
    }
}

async function geocodeDestination(destination) {
    try {
        // Using Nominatim (OpenStreetMap's geocoding service)
        const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(destination)}`);
        const data = await response.json();
        
        if (data && data.length > 0) {
            const lat = parseFloat(data[0].lat);
            const lon = parseFloat(data[0].lon);
            map.setView([lat, lon], 10);
            
            // Add destination marker
            L.marker([lat, lon])
                .addTo(map)
                .bindPopup(`<strong>${destination}</strong>`)
                .openPopup();
        }
    } catch (error) {
        console.error('Error geocoding destination:', error);
    }
}