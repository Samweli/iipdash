import maplibregl from 'maplibre-gl';

// Initialize MapLibre GL JS
const map = new maplibregl.Map({
    container: 'map', // ID of the div
    style: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json', // Positron Basemap
    center: [27.5, -10.0], // Center over [Malawi, Zambia, and DRC]
    zoom: 5,
});

// Add zoom & rotation controls
map.addControl(new maplibregl.NavigationControl());
