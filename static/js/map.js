/*
static/js/map.js

Initializes a Leaflet map and adds markers from the `restaurantsData` variable
which the template sets via Jinja.

Expected structure of restaurantsData: an array of objects with:
- id, name, address, latitude, longitude
*/

(function() {
    if (typeof restaurantsData === 'undefined') {
        console.error('restaurantsData is undefined. Map will not render.');
        return;
    }

    // Provide a sensible fallback center (NYC)
    const center = [40.7128, -74.0060];
    const map = L.map('map').setView(center, 13);

    // OpenStreetMap tiles (free)
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Add markers
    restaurantsData.forEach(r => {
        if (r.latitude && r.longitude) {
            const marker = L.marker([r.latitude, r.longitude]).addTo(map);
            const popupHtml = `
                <div style="min-width:200px">
                    <strong>${r.name}</strong><br/>
                    ${r.address || ''}<br/>
                    <a href="/restaurants/${r.id}">View details</a>
                </div>
            `;
            marker.bindPopup(popupHtml);
        }
    });

    // If there are markers, adjust bounds to show them all
    const validCoords = restaurantsData.filter(r => r.latitude && r.longitude);
    if (validCoords.length > 0) {
        const latlngs = validCoords.map(r => [r.latitude, r.longitude]);
        map.fitBounds(latlngs, { padding: [40, 40] });
    }
})();