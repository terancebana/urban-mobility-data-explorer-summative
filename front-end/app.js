const API_BASE_URL = "http://127.0.0.1:5001/api";
let tripChart;

async function updateDashboard() {
    const boroughFilter = document.getElementById('boroughFilter');
    if (!boroughFilter) return;

    const borough = boroughFilter.value;
    const totalTripsEl = document.getElementById('totalTrips');
    const avgSpeedEl = document.getElementById('avgSpeed');
    const avgFareEl = document.getElementById('avgFare');


    totalTripsEl.innerText = "Loading...";

    try {

        const response = await fetch(`${API_BASE_URL}/trips?borough=${borough}&limit=100`);
        const data = await response.json();

        if (data.length > 0) {

            totalTripsEl.innerText = data.length.toLocaleString();


            const avgSpeed = data.reduce((acc, row) => acc + (row.avg_speed_kmh || 0), 0) / data.length;
            const avgFare = data.reduce((acc, row) => acc + (row.fare_amount || 0), 0) / data.length;

            avgSpeedEl.innerText = avgSpeed.toFixed(1) + " km/h";
            avgFareEl.innerText = "$" + avgFare.toFixed(2);


            renderChart(data);
        } else {
            totalTripsEl.innerText = "0";
            avgSpeedEl.innerText = "--";
            avgFareEl.innerText = "--";
        }
    } catch (error) {
        console.error("Dashboard Update Failed:", error);
        totalTripsEl.innerText = "Error";
    }
}




function renderChart(data) {
    const ctx = document.getElementById('tripChart').getContext('2d');


    if (tripChart) { tripChart.destroy(); }


    const hourCounts = {};
    data.forEach(trip => {
        const hour = trip.pickup_hour;
        hourCounts[hour] = (hourCounts[hour] || 0) + 1;
    });

    tripChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(hourCounts).sort((a, b) => a - b),
            datasets: [{
                label: 'Number of Trips',
                data: Object.values(hourCounts),
                backgroundColor: 'rgba(0, 0, 0, 0.1)',
                borderColor: 'rgba(0, 0, 0, 1)',
                borderWidth: 1
            }]
        },
        options: { responsive: true, scales: { y: { beginAtZero: true } } }
    });
}


document.addEventListener('DOMContentLoaded', () => {

    updateDashboard();

    const applyBtn = document.getElementById('applyFilters');
    if (applyBtn) {
        applyBtn.addEventListener('click', updateDashboard);
    }


    const algoBtn = document.getElementById('loadAlgorithmData');
    if (algoBtn) {
        algoBtn.addEventListener('click', async () => {
            const boroughEl = document.getElementById('boroughFilter');
            const borough = boroughEl ? boroughEl.value : 'Manhattan';
            const response = await fetch(`${API_BASE_URL}/top_fares?borough=${borough}`);
            const data = await response.json();
            const tbody = document.getElementById('algorithmResults');
            tbody.innerHTML = data.map(trip => `
                <tr>
                    <td>${trip.pickup_borough}</td>
                    <td>${trip.dropoff_borough}</td>
                    <td>$${trip.fare_amount.toFixed(2)}</td>
                </tr>
            `).join('');
        });
    }


    if (document.getElementById('map')) {
        const map = L.map('map').setView([40.7128, -74.0060], 11);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

        const boroughColors = {
            'Manhattan': '#ef4444',
            'Brooklyn': '#f59e0b',
            'Queens': '#10b981',
            'Bronx': '#3b82f6',
            'Staten Island': '#8b5cf6',
            'EWR': '#6b7280'
        };

        fetch('../assets/taxi_zones.json')
            .then(res => res.json())
            .then(geojsonData => {
                L.geoJSON(geojsonData, {
                    style: (feature) => ({
                        fillColor: boroughColors[feature.properties.borough] || '#6b7280',
                        color: "white",
                        weight: 0.5,
                        fillOpacity: 0.5
                    }),
                    onEachFeature: (feature, layer) => {
                        layer.bindPopup(`
                            <div style="color: #0c1427; font-family: sans-serif;">
                                <strong>Zone:</strong> ${feature.properties.zone}<br>
                                <strong>Borough:</strong> ${feature.properties.borough}
                            </div>
                        `);
                        layer.on('mouseover', function() { this.setStyle({ fillOpacity: 0.8 }); });
                        layer.on('mouseout', function() { this.setStyle({ fillOpacity: 0.5 }); });
                    }
                }).addTo(map);
            });
    }


    const tripContainer = document.getElementById('tripListContainer');
    if (tripContainer) {
        let currentPage = 0;
        const searchInput = document.getElementById('tripSearch');
        const searchBtn = document.getElementById('searchBtn');
        const prevBtn = document.getElementById('prevPage');
        const nextBtn = document.getElementById('nextPage');
        const pageNumEl = document.getElementById('pageNumber');

        async function fetchTrips(page = 0) {
            const borough = searchInput.value || '';
            const offset = page * 10;
            const url = `${API_BASE_URL}/trips?borough=${borough}&limit=10&offset=${offset}`;

            tripContainer.innerHTML = '<p class="loading-text">Loading trips...</p>';

            try {
                const response = await fetch(url);
                const trips = await response.json();

                if (trips.length === 0) {
                     tripContainer.innerHTML = '<p class="loading-text">No trips found matching criteria.</p>';
                     return;
                }

                tripContainer.innerHTML = trips.map(trip => `
                    <div class="trip-card ${trip.is_overpaying ? 'overpaying' : ''}" onclick="this.classList.toggle('expanded')">
                        <div class="trip-header">
                            <div class="trip-id">Borough: ${trip.pickup_borough || 'Unknown'}
                                ${trip.is_overpaying ? '<span class="overpaying-badge">⚠️ Overpaying</span>' : ''}
                            </div>
                            <div class="trip-status">${trip.payment_type === 1 ? 'Credit Card' : 'Cash'}</div>
                        </div>
                        <div class="trip-details">
                            <div class="trip-detail-item">
                                <span class="trip-detail-label">Distance</span>
                                <span class="trip-detail-value">${trip.trip_distance} mi</span>
                            </div>
                            <div class="trip-detail-item">
                                <span class="trip-detail-label">Fare</span>
                                <span class="trip-detail-value">$${trip.fare_amount}</span>
                            </div>
                            <div class="trip-detail-item">
                                <span class="trip-detail-label">Fare/Mile</span>
                                <span class="trip-detail-value">$${(trip.fare_per_mile || 0).toFixed(2)}</span>
                            </div>
                        </div>

                        <div class="expand-hint">Click to see route details ↓</div>

                        <div class="trip-details-expandable">
                            <div class="trip-route">
                                <div style="margin-bottom: 8px;">
                                    <strong>Pickup Time:</strong> ${trip.tpep_pickup_datetime}
                                </div>
                                <div style="margin-bottom: 8px;">
                                    <strong>Dropoff Time:</strong> ${trip.tpep_dropoff_datetime}
                                </div>
                                <div style="margin-bottom: 8px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 8px;">
                                    <strong>From:</strong> ${trip.pickup_zone || 'N/A'}
                                </div>
                                <div>
                                    <strong>To:</strong> ${trip.dropoff_zone || 'N/A'}
                                </div>
                            </div>
                        </div>
                    </div>
                `).join('');


                pageNumEl.innerText = `Page ${page + 1}`;
                prevBtn.disabled = page === 0;
                prevBtn.style.opacity = page === 0 ? "0.5" : "1";

            } catch (e) {
                console.error(e);
                tripContainer.innerHTML = '<p class="loading-text">Error loading trips. Ensure backend is running.</p>';
            }
        }


        if (searchBtn) {
            searchBtn.addEventListener('click', () => { currentPage = 0; fetchTrips(0); });
        }

        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') { currentPage = 0; fetchTrips(0); }
        });

        prevBtn.addEventListener('click', () => {
            if (currentPage > 0) {
                currentPage--;
                fetchTrips(currentPage);
            }
        });

        nextBtn.addEventListener('click', () => {
            currentPage++;
            fetchTrips(currentPage);
        });


        fetchTrips(0);
    }


    if (document.getElementById('fareChart')) {
        loadFareAnalytics();
    }
});

async function loadFareAnalytics() {
    const boroughFilter = document.getElementById('boroughFilter');
    const borough = boroughFilter ? boroughFilter.value : '';

    try {
        const response = await fetch(`${API_BASE_URL}/trips?borough=${borough}&limit=200`);
        const trips = await response.json();

        if (trips.length === 0) return;

        const fares = trips.map(t => t.fare_per_mile).filter(v => v > 0);
        const avg = fares.length ? fares.reduce((a, b) => a + b, 0) / fares.length : 0;
        const stdDev = fares.length > 1
            ? Math.sqrt(fares.map(v => (v - avg) ** 2).reduce((a, b) => a + b, 0) / fares.length)
            : 0;
        const outliers = trips.filter(t => t.is_overpaying).length;


        if (document.getElementById('avgFareAnalytics')) {
            document.getElementById('avgFareAnalytics').innerText = `$${avg.toFixed(2)}`;
            document.getElementById('stdDevFare').innerText = `$${stdDev.toFixed(2)}`;
            document.getElementById('outlierCount').innerText = outliers;
        }

        renderAnalyticsCharts({
            avg,
            stdDev,
            outliers,
            normal: trips.length - outliers
        });

    } catch (e) {
        console.error("Analytics Error:", e);
    }
}

function renderAnalyticsCharts(stats) {
    const fareCtx = document.getElementById('fareChart').getContext('2d');
    const outlierCtx = document.getElementById('outlierPieChart').getContext('2d');

    new Chart(fareCtx, {
        type: 'bar',
        data: {
            labels: ['Avg Fare/Mile', 'Std Dev'],
            datasets: [{
                label: 'Fare Statistics ($)',
                data: [stats.avg, stats.stdDev],
                backgroundColor: ['#3b82f6', '#ef4444'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } }
        }
    });

    new Chart(outlierCtx, {
        type: 'pie',
        data: {
            labels: ['Normal Trips', 'Outliers'],
            datasets: [{
                data: [stats.normal, stats.outliers],
                backgroundColor: ['#22c55e', '#ef4444'],
                borderWidth: 0
            }]
        },
        options: { responsive: true }
    });
}