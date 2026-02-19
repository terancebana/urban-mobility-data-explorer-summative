//Api endpoint
const API_BASE = "http://localhost:5000/api/trips";
let currentOffset = 0;
let currentLimit = 10;

// Utility: formatting numbers to fixed decimals or show N/A when not valid
function formatNumber(value, decimals = 2) {
  return (value !== null && value !== undefined && !isNaN(value))
    ? Number(value).toFixed(decimals)
    : "N/A";
}

// Compute summary from trips array
function computeSummary(trips, borough) {
  //When there are no trips found,  return summary with nulls and os.
  if (!trips || !trips.length) {
    return {
      borough: borough || "All",
      average_fare_per_mile: null,
      std_dev_fare_per_mile: null,
      total_trips: 0,
      outlier_count: 0
    };
  }

  const fares = trips.map(t => t.fare_per_mile).filter(v => v !== null);
  const avg = fares.length ? fares.reduce((a, b) => a + b, 0) / fares.length : null;
  const stdDev = fares.length > 1
    ? Math.sqrt(fares.map(v => (v - avg) ** 2).reduce((a, b) => a + b, 0) / fares.length)
    : null;
  const outliers = trips.filter(t => t.is_overpaying).length;

  return {
    borough: borough || trips[0].pickup_borough || "All",
    average_fare_per_mile: avg,
    std_dev_fare_per_mile: stdDev,
    total_trips: trips.length,
    outlier_count: outliers
  };
}

// Load trips from API
async function loadTrips() {
  const borough = document.getElementById("borough").value;
  currentLimit = parseInt(document.getElementById("limit").value) || 100;
  currentOffset = parseInt(document.getElementById("offset").value) || 0;

  const url = `${API_BASE}?borough=${encodeURIComponent(borough)}&limit=${currentLimit}&offset=${currentOffset}`;

  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }

    const data = await response.json();
    console.log("API response:", data); // Debugging

    // If backend provides trips array, use it; otherwise assume data is trips
    const trips = data.trips || data;

    // Compute summary from trips by calling the computeSummary function and render both summary and trips
    const summary = computeSummary(trips, borough);
    if (document.getElementById("summary-content")) {
      renderSummary(summary);
    }

    renderTrips(trips);

  } catch (err) {
    console.error("Error fetching trips:", err);
    document.getElementById("summary-content").innerHTML =
      `<p style="color:red;">Failed to load trips.</p>`;
    document.getElementById("trips-body").innerHTML = "Hey";
  }
}

// Render summary section
function renderSummary(summary = {}) {
  document.getElementById("summary-content").innerHTML = `
    <p>Borough: ${summary.borough || "All"}</p>
    <p>Average Fare per Mile: ${formatNumber(summary.average_fare_per_mile)}</p>
    <p>Std Dev Fare per Mile: ${formatNumber(summary.std_dev_fare_per_mile)}</p>
    <p>Total Trips: ${summary.total_trips || 0}</p>
    <p>Outlier Count: ${summary.outlier_count || 0}</p>
  `;
}

// Render trips table
function renderTrips(trips = []) {
  const tbody = document.getElementById("trips-body");
  tbody.innerHTML = "";

  if (!trips.length) {
    tbody.innerHTML = `<tr><td colspan="4">No trips found</td></tr>`;
    return;
  }

  trips.forEach(trip => {
    const row = document.createElement("tr");
    if (trip.is_overpaying) row.classList.add("outlier");

    row.innerHTML = `
      <td>${trip.pickup_zone}</td>
      <td>${trip.dropoff_zone}</td>
      <td>${trip.tpep_pickup_datetime}</td>
      <td>${trip.tpep_dropoff_datetime}</td>
      <td>${trip.trip_distance}</td>
      <td>${trip.fare_amount}</td>
      <td>${trip.fare_per_mile}</td>
      <td>${trip.is_overpaying ? "YES" : "NO"}</td>
    `;
    tbody.appendChild(row);
  });
}

function nextPage() { 
  currentOffset += currentLimit;
  document.getElementById("offset").value = currentOffset; 
  loadTrips(); 
} 

function prevPage() {
  currentOffset = Math.max(0, currentOffset - currentLimit); 
  document.getElementById("offset").value = currentOffset; 
  loadTrips(); 
}

// Load analytics (for analytics.html) 
async function loadAnalytics() { 
  const fareCanvas = document.getElementById("fareChart"); 
  if (!fareCanvas) return; // Not on analytics.html 
  try { 
    const response = await fetch(`${API_BASE}?limit=100&offset=0`); 
    if (!response.ok) throw new Error(`Server returned ${response.status}`); 
    
    const data = await response.json(); 
    const trips = data.trips || data; 
    const summary = computeSummary(trips); 
    
    renderCharts(summary); 
  } catch (err) { 
    console.error("Error loading analytics:", err); 
  } 
} 

// Render charts (analytics.html) 
function renderCharts(summary) {
  const fareCtx = document.getElementById("fareChart").getContext("2d"); 
  new Chart(fareCtx, { 
    type: "bar", 
    data: { 
      labels: ["Average Fare per Mile", "Std Dev Fare per Mile"], 
      datasets: [{ 
        label: "Fare Stats", 
        data: [summary.average_fare_per_mile, summary.std_dev_fare_per_mile], 
        backgroundColor: ["#4CAF50", "#FF9800"] 
        
      }] 
    } 
  }); 
  
  const outlierCtx = document.getElementById("outlierChart").getContext("2d"); 
  new Chart(outlierCtx, { 
    type: "pie", 
    data: { 
      labels: ["Outliers", "Normal Trips"], 
      datasets: [{ 
        data: [summary.outlier_count, summary.total_trips - summary.outlier_count], 
        backgroundColor: ["#F44336", "#2196F3"] 
      }] 
    } 
  }); 
}

// Auto-load trips on page load
document.addEventListener("DOMContentLoaded", () => {
  loadTrips();
  loadAnalytics();
});
