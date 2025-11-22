(function() {
    // Use global restaurantsData
    if (!window.restaurantsData || restaurantsData.length === 0) {
        console.log("No restaurant data to display.");
        return;
    }

    const center = [
        restaurantsData[0].latitude || 40.7128,
        restaurantsData[0].longitude || -74.0060
    ];
    const map = L.map('map').setView(center, 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    const markers = [];
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

    if (markers.length > 0) {
        const group = new L.featureGroup(markers);
        map.fitBounds(group.getBounds(), { padding: [40, 40] });
    }
})();