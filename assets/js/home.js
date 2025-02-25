import maplibregl from 'maplibre-gl';
import Chart from 'chart.js/auto';

// Initialize MapLibre GL JS
const map = new maplibregl.Map({
    container: 'map', // ID of the div
    style: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json', // Positron Basemap
    center: [27.5, -10.0], // Center over [Malawi, Zambia, and DRC]
    zoom: 5,
});

// Add zoom & rotation controls
map.addControl(new maplibregl.NavigationControl());

//
// Sample school fiber node stats bar chart
//

document.addEventListener('DOMContentLoaded', () => {
  const ctx = document
    .getElementById('school-fiber-node-stats-bar-chart')
    .getContext('2d');

  const data = {
    labels: [' '], // Empty label to remove Y-axis text
    datasets: [
      { label: '10KM', data: [117], backgroundColor: '#007FFF' },
      { label: '20KM', data: [63], backgroundColor: '#82A5FF' },
      { label: '30KM', data: [115], backgroundColor: '#BFCCFF' },
      { label: ' ', data: [23], backgroundColor: '#D9D9D9' },
    ],
  };

  const config = {
    type: 'bar',
    data,
    options: {
      indexAxis: 'y', // Horizontal bar
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { stacked: true, display: false },
        y: { stacked: true, display: false },
      },
      plugins: {
        legend: {
          display: true,
          position: 'top',
          labels: { boxWidth: 12, font: { size: 12 }, padding: 10 },
        },
        tooltip: { enabled: false },
      },
    },
  };

  // Initialize Chart
  new Chart(ctx, config); // eslint-disable-line no-new
});

//
// Sample school fiber node stats histogram chart
//

document.addEventListener('DOMContentLoaded', () => {
  const ctx = document
    .getElementById('school-fiber-node-stats-histogram-chart')
    .getContext('2d');

  // Simulated data: Number of schools at different distance ranges (0-70 km)
  // Generate more data points for very thin bars (0-70 km in 1 km intervals)
  const distances = Array.from({ length: 71 }, (_, i) => `${i} km`);
  const schoolCounts = Array.from({ length: 71 }, () =>
    Math.floor(Math.random() * 100),
  ); // Random data for demo

  const data = {
    labels: distances,
    datasets: [
      {
        label: 'Number of Schools',
        data: schoolCounts,
        backgroundColor: '#007FFF',
        // borderRadius: 5, // Rounded bar edges for a sleek look
        barPercentage: 0.8, // Reduce bar width
        categoryPercentage: 0.8, // Reduce space between bars
      },
    ],
  };

  const config = {
    type: 'bar',
    data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        // x: { display: false }, // Hide X-axis
        x: {
          min: 0, // Ensure the scale starts at 0
          max: 70, // Ensure the scale ends at 70
          ticks: {
            display: true,
            font: { weight: 'bold', size: 12 }, // Make labels bold
            callback: function (value, index, values) {
              if (value === 0) return '0 KM';
              if (value === 70) return '70 KM'; // Force "70 KM" to appear
              return ''; // Hide other labels
            },
            autoSkip: false, // Prevent skipping labels
            maxRotation: 0, // Keep labels horizontal
            minRotation: 0,
          },
          grid: { display: false }, // Hide vertical grid lines
        },
        y: { display: false }, // Hide Y-axis
      },
      plugins: {
        legend: { display: false }, // Hide legend (only one dataset)
        tooltip: { enabled: false }, // Enable tooltips
      },
    },
  };

  // Initialize Chart
  new Chart(ctx, config); // eslint-disable-line no-new
});
