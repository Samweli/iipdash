import maplibregl from 'maplibre-gl';
import * as utils from './utils';


 /**
 * Create a popup for the education institutions layer features.
 *
 *
 * This:
 *
 * - Fetch `country` name based on clicked education institution
 * - Fetch `region` name based on clicked education institution
 * - Display a popup with education institution properties
 */
export const educationInstitutionPopup = function (event, countries){
    const countryName = countries[event.features[0].properties.country];
    const name = `${event.features[0].properties.name}`;
    const selectedRegion = event.features[0].properties.administrative_area_name;

    let avgDistance = utils.meters2km(event.features[0].properties.fon_distance);
    if (isNaN(avgDistance)) {
        avgDistance = '-';
    }

    const popup = new maplibregl.Popup()
        .setLngLat(event.lngLat)
        .setHTML(
            `<div class="card shadow-sm border-0 rounded-3">
              <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center rounded-top-3 px-4 py-3">
                <h5 class="mb-0 text-truncate fw-bold" >${name}</h5>
              </div>
              <div class="card-body bg-light text-dark px-4 py-3">
                <div class="d-flex align-items-start mb-3">
                  <span class="me-3 fs-6 text-primary">🗺️</span>
                  <div class="flex-grow-1">
                    <div class="text-muted small">Administrative area</div>
                    <div class="fw-semibold text-uppercase fs-6">${selectedRegion}</div>
                  </div>
                </div>
                <div class="d-flex align-items-start">
                  <span class="me-3 fs-6 text-primary">📏</span>
                  <div class="flex-grow-1">
                    <div class="text-muted small">Distance to the nearest fiber node(km)</div>
                    <div class="fw-semibold fs-6">${avgDistance}</div>
                  </div>
                </div>
              </div>
            </div>`,
        );

    return popup;
};



/**
 * Create a popup for the cell towers- layer features.
 *
 *
 * This:
 *
 * - Fetch `country` name based on clicked cell tower
 * - Fetch `region` name based on clicked cell tower
 * - Fetch `network_type` name based on clicked cell tower
 * - Fetch `range` value based on clicked cell tower
 * - Display a popup with cell tower properties
 */
export const cellTowerPopup = function (event, countries){
    const selectedRegion = event.features[0].properties.administrative_area_name;
    const networkType = event.features[0].properties.network_type;
    const range = event.features[0].properties.range;

    const popup = new maplibregl.Popup()
        .setLngLat(event.lngLat)
        .setHTML(
            `<div class="card shadow-sm border-0 rounded-3">
              <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center rounded-top-3 px-4 py-3">
                <h5 class="mb-0 text-truncate fw-bold">Cell tower</h5>
              </div>
              <div class="card-body bg-light text-dark px-4 py-3">
                <div class="d-flex align-items-start mb-3">
                  <span class="me-3 fs-6 text-primary">🗺️</span>
                  <div class="flex-grow-1">
                    <div class="text-muted small">Administrative area</div>
                    <div class="fw-semibold text-uppercase fs-6">${selectedRegion}</div>
                  </div>
                </div>
                <div class="d-flex align-items-start">
                  <span class="me-3 fs-6 text-primary">📶</span>
                  <div class="flex-grow-1">
                    <div class="text-muted small">Network type</div>
                    <div class="fw-semibold fs-6">${networkType}</div>
                  </div>
                </div>
                <div class="d-flex align-items-start">
                  <span class="me-3 fs-6 text-primary">📡</span>
                  <div class="flex-grow-1">
                    <div class="text-muted small">Range (m)</div>
                    <div class="fw-semibold fs-6">${range}</div>
                  </div>
                </div>
              </div>
            </div>`,
        );
    return popup;
};

/**
 * Create a popup for the health facilities layer features.
 *
 *
 * This:
 *
 * - Fetch `country` name based on clicked health facility
 * - Fetch `region` name based on clicked health facility
 * - Fetch `amenity` name from the clicked health facility

 * - Display a popup with health facility properties
 */
export const healthFacilityPopup = function (event, countries){
    const name = `${event.features[0].properties.name}`;
    const selectedRegion = event.features[0].properties.administrative_area_name;
    const amenity = event.features[0].properties.amenity;

    const popup = new maplibregl.Popup()
        .setLngLat(event.lngLat)
        .setHTML(
            `<div class="card shadow-sm border-0 rounded-3">
              <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center rounded-top-3 px-4 py-3">
                <h5 class="mb-0 text-truncate fw-bold">${name}</h5>
              </div>
              <div class="card-body bg-light text-dark px-4 py-3">
                <div class="d-flex align-items-start mb-3">
                  <span class="me-3 fs-6 text-primary">🗺️</span>
                  <div class="flex-grow-1">
                    <div class="text-muted small">Administrative area</div>
                    <div class="fw-semibold text-uppercase fs-6">${selectedRegion}</div>
                  </div>
                </div>
                <div class="d-flex align-items-start">
                  <span class="me-3 fs-6 text-primary">🏢</span>
                  <div class="flex-grow-1">
                    <div class="text-muted small">Amenity</div>
                    <div class="fw-semibold fs-6">${amenity}</div>
                  </div>
                </div>
              </div>
            </div>`
        );

    return popup;
};

/**
 * Create a popup for the fiber nodes layer features.
 *
 *
 * This:
 *
 * - Fetch `country` name based on clicked fiber node
 * - Fetch `region` name based on clicked  fiber node
 * - Fetch `node_type` value of the clicked  fiber node

 * - Display a popup with  fiber node properties
 */
export const fiberNodePopup = function (event, countries){
    const selectedRegion = event.features[0].properties.administrative_area_name;
    const node_type = event.features[0].properties.node_type;

    const popup = new maplibregl.Popup()
        .setLngLat(event.lngLat)
        .setHTML(
            `<div class="card shadow-sm border-0 rounded-3">
              <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center rounded-top-3 px-4 py-3">
                <h5 class="mb-0 text-truncate fw-bold">Node</h5>
              </div>
              <div class="card-body bg-light text-dark px-4 py-3">
                <div class="d-flex align-items-start mb-3">
                  <span class="me-3 fs-6 text-primary">🗺️</span>
                  <div class="flex-grow-1">
                    <div class="text-muted small">Administrative area</div>
                    <div class="fw-semibold text-uppercase fs-6">${selectedRegion}</div>
                  </div>
                </div>
                <div class="d-flex align-items-start">
                  <span class="me-3 fs-6 text-primary">🪢</span>
                  <div class="flex-grow-1">
                    <div class="text-muted small">Node type</div>
                    <div class="fw-semibold fs-6">${node_type}</div>
                  </div>
                </div>
              </div>
            </div>`,
        );

    return popup;
};


/**
 * Create a popup for the internet speed layer features.
 *
 *
 * This:
 *
 * - Fetch `country` name based on clicked internet speed
 * - Fetch `region` name based on clicked  internet speed
 * - Fetch `speed` value based on clicked  internet speed
 * - Display a popup with  internet speed properties
 */
export const internetSpeedPopup = function (event, countries){
    const countryName = countries[event.features[0].properties.country];
    const name = event.features[0].properties.name;
    let speed = event.features[0].properties.mobile_speed;

    if (isNaN(speed)) {
        speed = '-';
    }


    const popup = new maplibregl.Popup()
        .setLngLat(event.lngLat)
        .setHTML(
            `<div class="card shadow-sm border-0 rounded-3">
              <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center rounded-top-3 px-4 py-3">
                <h5 class="mb-0 text-truncate fw-bold">Internet speed</h5>
              </div>
              <div class="card-body bg-light text-dark px-4 py-3">
                <div class="d-flex align-items-start mb-3">
                  <span class="me-3 fs-6 text-primary">
                    🌍
                  </span>
                  <div class="flex-grow-1">
                    <div class="text-muted small">Country</div>
                    <div class="fw-semibold text-uppercase fs-6">${countryName}</div>
                  </div>
                </div>
                <div class="d-flex align-items-start mb-3">
                  <span class="me-3 fs-6 text-primary">🗺️</span>
                  <div class="flex-grow-1">
                    <div class="text-muted small">Administrative area</div>
                    <div class="fw-semibold text-uppercase fs-6">${name}</div>
                  </div>
                </div>
                <div class="d-flex align-items-start">
                  <span class="me-3 fs-6 text-primary">
                    ⚡
                  </span>
                  <div class="flex-grow-1">
                    <div class="text-muted small">Speed</div>
                    <div class="fw-semibold fs-6">${speed}</div>
                  </div>
                </div>
              </div>
            </div>`,
        );

    return popup;
};


