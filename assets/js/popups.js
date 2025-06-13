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
            `<div class="card border-0">
                <div class="card-header text-bg-primary">
                  <h5 class="text-white pe-3">${name}</h5>
                </div>

                <div class="card-body">
                    <p class="text-uppercase fs-6 fw-light text-muted">
                        Country : ${countryName}
                    </p>
                    <p class="text-uppercase fs-6 fw-light text-muted">
                        Region : ${selectedRegion}
                    </p>
                    <p class="text-uppercase fs-6 fw-light text-muted">
                        Distance to the nearest fiber(km) : ${avgDistance}
                    </p>

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
    const countryName = countries[event.features[0].properties.country];
    const name = `${event.features[0].properties.name}`;
    const selectedRegion = event.features[0].properties.administrative_area_name;
    const networkType = event.features[0].properties.networkType;
    const range = event.features[0].properties.range;

    const popup = new maplibregl.Popup()
        .setLngLat(event.lngLat)
        .setHTML(
            `<div class="card border-0">
                <div class="card-header text-bg-primary">
                  <h5 class="text-white pe-3">${name}</h5>
                </div>

                <div class="card-body">
                    <p class="text-uppercase fs-6 fw-light text-muted">
                        Country : ${countryName}
                    </p>
                    <p class="text-uppercase fs-6 fw-light text-muted">
                        Region : ${selectedRegion}
                    </p>
                    <p class="text-uppercase fs-6 fw-light text-muted">
                        Network Type : ${networkType}
                    </p>
                    <p class="text-uppercase fs-6 fw-light text-muted">
                        Range : ${range}
                    </p>

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
    const countryName = countries[event.features[0].properties.country];
    const name = `${event.features[0].properties.name}`;
    const selectedRegion = event.features[0].properties.administrative_area_name;
    const amenity = event.features[0].properties.amenity;

    const popup = new maplibregl.Popup()
        .setLngLat(event.lngLat)
        .setHTML(
            `<div class="card border-0">
                <div class="card-header text-bg-primary">
                  <h5 class="text-white pe-3">${name}</h5>
                </div>

                <div class="card-body">
                    <p class="text-uppercase fs-6 fw-light text-muted">
                        Country : ${countryName}
                    </p>
                    <p class="text-uppercase fs-6 fw-light text-muted">
                        Region : ${selectedRegion}
                    </p>
                    <p class="text-uppercase fs-6 fw-light text-muted">
                        Amenity : ${amenity}
                    </p>

                </div>
            </div>`,
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
    const countryName = countries[event.features[0].properties.country];
    const selectedRegion = event.features[0].properties.administrative_area_name;
    const node_type = event.features[0].properties.node_type;

    const popup = new maplibregl.Popup()
        .setLngLat(event.lngLat)
        .setHTML(
            `<div class="card border-0">
                <div class="card-header text-bg-primary">
                  <h5 class="text-white pe-3">${name}</h5>
                </div>

                <div class="card-body">
                    <p class="text-uppercase fs-6 fw-light text-muted">
                        Country : ${countryName}
                    </p>
                    <p class="text-uppercase fs-6 fw-light text-muted">
                        Region : ${selectedRegion}
                    </p>
                    <p class="text-uppercase fs-6 fw-light text-muted">
                        Node Type : ${node_type}
                    </p>

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
    const selectedRegion = event.features[0].properties.administrative_area_name;
    const speed = event.features[0].properties.speed;

    const popup = new maplibregl.Popup()
        .setLngLat(event.lngLat)
        .setHTML(
            `<div class="card border-0">
                <div class="card-header text-bg-primary">
                  <h5 class="text-white pe-3">${name}</h5>
                </div>

                <div class="card-body">
                    <p class="text-uppercase fs-6 fw-light text-muted">
                        Country : ${countryName}
                    </p>
                    <p class="text-uppercase fs-6 fw-light text-muted">
                        Region : ${selectedRegion}
                    </p>
                    <p class="text-uppercase fs-6 fw-light text-muted">
                        Speed : ${speed}
                    </p>

                </div>
            </div>`,
        );

    return popup;
};


