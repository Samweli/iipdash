import _ from 'lodash';
import * as Vue from 'vue';
import maplibregl from 'maplibre-gl';

import * as settings from './conf';
import * as utils from './utils';
import * as maps from './maps';
import { fetchCountries, fetchRegions } from './api';

/**
 *  HazardDash Vue application.
 */
const HazardDash = {
    /**
     * Registers child components.
     */
    components: {},

    /**
     * Initializes the component's reactive data.
     */
    data: function () {
        return {
            _map: null,
            _mapId: '_hazard-map',
            mapLoaded: false,
            lookup: {
                administrative_area: '',
                country: '',
            },
            countries: { features: [] },
            countriesLookup: {},
            regions: { features: [] },
            regionOptions: { features: [] },
            selectedCountry: null,
            selectedRegion: null,
        };
    },

    /**
     * Defines computed properties derived from the component's data.
     */
    computed: {
        selectedLocation() {
            const locations = [];

            if (this.selectedRegion) {
                locations.push(this.selectedRegion.properties.name);
            }

            if (this.selectedCountry) {
                locations.push(this.selectedCountry.properties.name);
            } else if (this.selectedRegion) {
                locations.push(this.countriesLookup[this.selectedRegion.properties.country]);
            }

            return locations.join(', ');
        },

        summaryCSVDownloadURL() {
            const params = {
                country: this.lookup.country,
                uuid: this.lookup.administrative_area,
                level: settings.ADMINISTRATIVE_AREAS_REGION_LEVEL,
            };
            return utils.updateURLParams(`${settings.API_ROOT}<set-path-to-download-here>`, params);
        },
    },

    /**
     * Defines methods that handle user interactions and component logic.
     */
    methods: {
        // ---
        // Start: Init methods
        // ---

        /**
         * Load initial data.
         *
         * This loads:
         *
         * - Countries
         * - Regions
         */
        initData: async function () {
            const [countries, regions] = await Promise.all([fetchCountries(), fetchRegions()]);

            this.regions = _.cloneDeep(regions);
            this.regionOptions = _.cloneDeep(regions);

            this.countries = _.cloneDeep(countries);
            this.countries.features.forEach((feature) => {
                this.countriesLookup[feature.properties.country] = feature.properties.name;
            });
        },

        /**
         * Initalize `maplibregl.Map` and load layers.
         */
        initMap: async function () {
            const map = new maplibregl.Map({
                ...maps.basemap,
                container: this._mapId,
            });

            this._map = Vue.markRaw(map);

            this._map.on('load', async () => {
                this.mapLoaded = true;
                await this.addMapLayers();
                await this.addMouseEvents();
            });

            const navigationControl = new maplibregl.NavigationControl({
                visualizePitch: true,
                visualizeRoll: true,
                showZoom: true,
                showCompass: true,
            });
            map.addControl(navigationControl);
        },

        // ---
        // End: Init methods
        // ---

        // ---
        // Start: Add methods
        // ---

        /**
         * Add map layers.
         */
        addMapLayers: async function () {
            // map style sources
            const mapSources = await maps.getSources();

            // country boundaries layer
            this._map.addSource(maps.layers.countries.id, mapSources.countries);
            this._map.addLayer(maps.layers.countries);

            // regions boundaries layer
            const regionsLayer = _.merge({}, maps.layers.regions, {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addSource('regions', mapSources.regions);
            this._map.addLayer(regionsLayer);
        },

        /**
         * Handles cursor style for different mouse events on the map layers.
         *
         * This:
         *
         * - Change cursor style for `mouseenter` and `mouseleave` events on map layers.
         */
        addMouseEvents: async function () {},

        /**
         * Add map layers legend.
         */
        addMapLegend: async function () {},

        // ---
        // END: Add methods
        // ---

        // ---
        // Start: Update methods
        // ---

        /**
         * Update data.
         *
         * This:
         *
         * - Set current selected country
         * - Set current selected region
         */
        updateData: async function () {
            // Update selected country
            if (this.lookup.country) {
                this.selectedCountry = _.find(this.countries.features, ['properties.country', this.lookup.country]);
            } else {
                this.selectedCountry = null;
            }

            // Update selected region
            if (this.lookup.administrative_area) {
                this.selectedRegion = _.find(this.regions.features, { id: this.lookup.administrative_area });
            } else {
                this.selectedRegion = null;
            }
        },

        /**
         * Update map to fit the bounds
         *
         * This pans and zooms the map to contain its visible area within the specified geographical bounding box.
         *
         * This:
         *
         * - Fit map to current selected region or,
         * - Fit map to current selected country
         */
        updateMapFitBounds: async function (options = {}) {
            // Obtain bound box
            let bbox;

            // If there is region selected
            if (this.lookup.administrative_area && this.selectedRegion) {
                bbox = this.selectedRegion.properties.bbox;
            }
            // If there is country selected
            else if (this.lookup.country && this.selectedCountry) {
                bbox = this.selectedCountry.properties.bbox;
            }

            // Pan map to bounds
            if (bbox && (this.lookup.country || this.lookup.administrative_area)) {
                this.fitMapBounds(bbox, options);
            }

            // Restore exact map zoom and center
            else {
                this.resetMapBounds();
            }
        },

        /**
         * Update (set or unset) map filters and visibilities to control administrative boundaries layers.
         *
         * Controlled layers are:
         *
         * - `countries`
         * - `regions`.
         *
         * This:
         *
         * - Filter `country` layers based on current selected `country`
         * - Filter `regions` layers based on current selected `country` and `administrative_area`
         * - Toggle `regions` layer visibility based on current selected `administrative_area`
         */
        updateMapAdministrativeBoundaryLayers: async function () {
            // Update map filter based on current country
            if (this.lookup.country) {
                this._map.setFilter('countries', ['==', ['get', 'country'], this.lookup.country]);
            } else {
                this._map.setFilter('countries', null);
            }

            // Update map filter based on current administrative region
            if (this.lookup.administrative_area) {
                this._map.setFilter('regions', ['==', ['get', 'uuid'], this.lookup.administrative_area]);
                this._map.setLayoutProperty('regions', 'visibility', 'visible');
            } else {
                this._map.setLayoutProperty('regions', 'visibility', 'none');
                this._map.setFilter('regions', null);
            }
        },

        /**
         * Update (set filters, unset filters) map.
         *
         * This:
         *
         * - update map administrative boundary layers
         */
        updateMap: async function () {
            if (!this.mapLoaded) {
                return;
            }

            // filter, toggle visibility of map layers
            await this.updateMapAdministrativeBoundaryLayers();
        },

        /**
         * Update data and map.
         *
         * This:
         *
         * - Update data by calling `updateDate`
         * - Update map by calling `updateMap`
         * - Dispatch `'page-updated'` event
         */
        update: async function () {
            try {
                await this.updateData();
                await this.updateMap();

                const event = new Event('page-updated');
                window.dispatchEvent(event);
            } catch (e) {
                console.log(e); // eslint-disable-line no-console
            }
        },

        // ---
        // End: Update methods
        // ---

        // ---
        // Start: UI event handlers methods
        // ---

        /**
         * Update ui and data once country selected in top map pane country selection
         *
         * This:
         *
         * - Update regionOptions
         * - Update data and map by calling `update`
         * - Update map fit bounds by calling `updateMapFitBounds`
         */
        handleCountrySelected: async function () {
            // Clear current selected administrative region
            this.lookup.administrative_area = '';

            // Update `regionOptions` to country specific region
            if (this.lookup.country) {
                this.regionOptions.features = _.filter(this.regions.features, [
                    'properties.country',
                    this.lookup.country,
                ]);
            }

            // Update `regionOptions` to all regions
            else {
                this.regionOptions.features = [...this.regions.features];
            }

            // Update map and data
            await this.update();
            await this.updateMapFitBounds();
        },

        /**
         * Update ui and data once region selected in top map pane country selection
         *
         * This:
         *
         * - Update data and map by calling `update`
         * - Update map fit bounds by calling `updateMapFitBounds`
         */
        handleRegionSelected: async function () {
            await this.update();
            await this.updateMapFitBounds();
        },

        // ---
        // End: UI event handlers methods
        // ---

        // ---
        // Start: Map bounds control methods
        // ---

        /**
         * Fit a map to a bounding box
         */
        fitMapBounds(bbox, options = {}) {
            this._map.fitBounds(
                [
                    [bbox[0], bbox[1]],
                    [bbox[2], bbox[3]],
                ],
                options,
            );
        },

        /**
         * Restore default map zoom and center
         */
        resetMapBounds() {
            this.fitMapBounds(settings.MAP_DEFAULT_BBOX);
        },

        // ---
        // End: Map bounds control methods
        // ---
    },

    /**
     * Lifecycle hook called after the component has been mounted to the DOM.
     *
     * This:
     *
     * - Load initial data by calling `initData`
     * - Initalize map and load layers by calling `initMap`
     * - Update data and map by calling `update`
     */
    mounted: async function () {
        await this.initData();
        await this.initMap();
        await this.update();
    },

    /**
     * Lifecycle hook called after the component has updated its DOM tree due to a reactive state change.
     */
    updated: async function () {},
};

// Create a new Vue application instance using the HazardDash root component.
const app = Vue.createApp(HazardDash);

// Mount the `HazardDash` Vue application to the DOM element with the ID '_hazard-dash'.
app.mount('#_hazard-dash');
