(function() {
    // Use global restaurantsData
    if (!window.restaurantsData || restaurantsData.length === 0) {
        console.log("No restaurant data to display.");
        return;
    }

    // Default center
    const center = [
        restaurantsData[0].latitude || 39.942178,
        restaurantsData[0].longitude || -75.166133
    ];
    const map = L.map('map').setView(center, 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    const markers = [];

    // Add restaurant markers
    restaurantsData.forEach(r => {
        if (r.latitude && r.longitude) {
            const marker = L.marker([r.latitude, r.longitude]).addTo(map);
            marker.bindPopup(`
                <div style="min-width:200px">
                    <strong>${r.name}</strong><br/>
                    ${r.address || ''}<br/>
                    <a href="/restaurants/${r.id}">View details</a>
                </div>
            `);
            markers.push(marker);
        }
    });

    // Add "You Are Here" marker at the center
    const centerMarker = L.marker(center, {
        icon: L.icon({
            iconUrl: '/static/images/you_are_here.png', // optional custom icon
            iconSize: [30, 30],
            iconAnchor: [15, 30]
        })
    }).addTo(map);
    centerMarker.bindPopup('<strong>You are here</strong>').openPopup();

    // Adjust bounds to include all restaurant markers + center marker
    const group = new L.featureGroup([...markers, centerMarker]);
    map.fitBounds(group.getBounds(), { padding: [40, 40] });
})();