import _ from 'lodash';
import * as Vue from 'vue';
import maplibregl from 'maplibre-gl';
import axios from 'axios';

import * as settings from './conf';
import * as utils from './utils';
import * as maps from './maps';
import { fetchCountries, fetchRegions } from './api';
import Chart from 'chart.js/auto';
import * as chartsConfig from './charts_config.js';


const HAZARD_TYPES = ['cyclone', 'flood', 'drought', 'heat'];
const URBANICITY_TYPE_ALL = ''

const POPULATION_EXPOSED_PERCENT = 'population_exposed_percent';

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
            hazardExposureAggregates: {},
            regionsHazardExposure: { features: [] },
            selectedCountry: null,
            selectedRegion: null,
            summaryLayerActive: true,
            mapSidebarTabsDetailsTabActive: false,
            secondaryFilters: {
                selectedHazardTypes: [...HAZARD_TYPES],
                selectedUrbanicityType: URBANICITY_TYPE_ALL, // or urban and rural
                selectedPopulationExposed: POPULATION_EXPOSED_PERCENT, // or population_exposed_ev_percent
            },
            charts: {
                hazardExposureSummary: {
                    id: 'hazard-exposure-summary-chart',
                },
                regionsHazardExposureSummary: {
                    id: 'regions-hazard-exposure-chart',
                },
            },
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
            return utils.updateURLParams(`${settings.API_ROOT}administrative/areas-hazards-exposure/download`, params);
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

            // Relative wealth index layer
            const relativeWealthIndexLayer = _.merge({}, maps.layers['relative-wealth-index'], {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addSource('relative-wealth-index', mapSources['relative-wealth-index']);
            this._map.addLayer(relativeWealthIndexLayer);

            // High resolution population density layer
            const populationDensityHDLayer = _.merge({}, maps.layers['population-density-hd'], {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addSource('population-density-hd', mapSources['population-density-hd']);
            this._map.addLayer(populationDensityHDLayer);

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

            // hazard exposure aggregations
            try {
                const hazardExposureAggregates = await axios.get(
                    `${settings.API_ROOT}hazards/hazard-exposures/aggregates/`,
                    {
                        params: {
                             ...this.lookup,
                             administrative_area_level: 3,
                             hazard_code_in: this.secondaryFilters.selectedHazardTypes.join(','),
                             urbanization_degree_group: this.secondaryFilters.selectedUrbanicityType
                        },
                    },
                );
                this.hazardExposureAggregates = hazardExposureAggregates.data;
            } catch (e) {
                console.log(e); // eslint-disable-line no-console
            }

            // hazard per region
            try {
                const regionsHazardExposure = await axios.get(`${settings.API_ROOT}administrative/areas-hazards-exposure/`, {
                    params: {
                        country: this.lookup.country || '',
                        administrative_area_level: 3,
                        exclude_geometry: true,
                        hazard_code_in: this.secondaryFilters.selectedHazardTypes.join(','),
                        urbanization_degree_group: this.secondaryFilters.selectedUrbanicityType

                    },
                });
                this.regionsHazardExposure = regionsHazardExposure.data;
            } catch (e) {
                console.log(e); // eslint-disable-line no-console
            }

            // TODO: handle secondary filters and selected legend layer
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
         * Update (set or unset) map filters and visibilities to control underlying data layers.
         *
         * Controlled layers are:
         *
         * - `relative-wealth-index`
         * - `population-density-hd`.
         *
         * This:
         *
         * - Filter underlying data layers based on current selected `country` and `region` (i.e `administrative_area`)
         * - Toggle underlying data layers visibility when `summaryLayerActive` toggled to `false`
         */
        updateMapUnderlyingDataLayers: async function () {
            // Update map filter based on current country
            if (this.lookup.country) {
                this._map.setFilter('relative-wealth-index', ['==', ['get', 'country'], this.lookup.country]);
                this._map.setFilter('population-density-hd', ['==', ['get', 'country'], this.lookup.country]);
            } else {
                this._map.setFilter('relative-wealth-index', null);
                this._map.setFilter('population-density-hd', null);
            }

            // Update map filter based on current administrative region
            if (this.lookup.administrative_area) {
                this._map.setFilter('relative-wealth-index', [
                    '==',
                    ['get', 'administrative_area_uuid'],
                    this.lookup.administrative_area,
                ]);
                this._map.setFilter('population-density-hd', [
                    '==',
                    ['get', 'administrative_area_uuid'],
                    this.lookup.administrative_area,
                ]);
            }

            // Toggle underlying data layers visibility when `summaryLayerActive` toggled to `false`
            if (this.summaryLayerActive) {
                this._map.setLayoutProperty('relative-wealth-index', 'visibility', 'none');
                this._map.setLayoutProperty('population-density-hd', 'visibility', 'none');
            } else {
                this._map.setLayoutProperty('relative-wealth-index', 'visibility', 'visible');
                this._map.setLayoutProperty('population-density-hd', 'visibility', 'visible');
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
            await this.updateMapUnderlyingDataLayers();

            // TODO: handle secondary filters and selected legend layer
        },

        updateCharts() {
            // summary hazard exposure bar

            const hazardExposureSummaryData = {
                labels: [' '], // Empty label to remove Y-axis text
                datasets: [
                    {
                        label: 'Population exposed',
                        data: [this.hazardExposureAggregates[this.secondaryFilters.selectedPopulationExposed]],
                        backgroundColor: '#007FFF',
                    },
                    {
                        label: 'Population not exposed',
                        data: [100 - this.hazardExposureAggregates[this.secondaryFilters.selectedPopulationExposed]],
                        backgroundColor: '#D9D9D9',
                    },
                ],
            };

            const hazardExposureSummaryConfig = {
                ...chartsConfig.hazardExposureSummary,
                data: hazardExposureSummaryData,
            };

            this.clearChart(this.charts.hazardExposureSummary.id);
            const hazardExposureSummaryCtx = document
                .getElementById(this.charts.hazardExposureSummary.id)
                .getContext('2d');

            new Chart(hazardExposureSummaryCtx, hazardExposureSummaryConfig); // eslint-disable-line no-new


            // regions hazard exposure
            const regionsHazardExposureData = {
                datasets: [
                    {
                        label: '',
                        data: this.regionsHazardExposure.features.map((coverage) => {
                            return {
                                x: this.round(coverage.properties.rwi_population_weighted, 2),
                                y: this.round(coverage.properties[`${this.secondaryFilters.selectedPopulationExposed}`], 2),
                                uuid: coverage.id,
                            };
                        }),
                        backgroundColor: (context) => {
                            const index = context.dataIndex;
                            const value = context.dataset.data[index];

                            if (value.uuid === this.selectedRegion?.id) {
                                return settings.COLOR_PRIMARY;
                            }

                            return 'rgba(100, 100, 100, 0.5)';
                        },
                        pointRadius: 4,
                        pointHoverRadius: 4.5,
                    },
                ],
            };

            const regionsHazardExposureConfig = {
                ...chartsConfig.regionsHazardExposure,
                data: regionsHazardExposureData,
            };

            this.clearChart(this.charts.regionsHazardExposureSummary.id);
            const regionsHazardExposureCtx = document
                .getElementById(this.charts.regionsHazardExposureSummary.id)
                .getContext('2d');
            new Chart(regionsHazardExposureCtx, regionsHazardExposureConfig); // eslint-disable-line no-new
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
                await this.updateCharts();

                const event = new Event('page-updated');
                window.dispatchEvent(event);
            } catch (e) {
                console.log(e); // eslint-disable-line no-console
            }
        },

        clearChart(elementID) {
            const ctx = document.getElementById(elementID);

            try {
                Chart.getChart(ctx).destroy();
            } catch (e) {
                // chart didn't exist yet
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
         * Update ui and data once region selected in top map pane region selection
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

        /**
         * Update ui, data and map when toggling between underlying data layers
         * and summary layer in top map pane toggle summary layer button
         *
         * This:
         *
         * - Set/unset visibility of summary layer
         * - Set/unset visibility of underlying data layers
         */
        handleSummaryLayerToggled: async function () {
            // TODO: ensure 'areas-hazard' layer is loaded
            const summaryVisibility = this._map.getLayoutProperty('areas-hazard', 'visibility');
            if (summaryVisibility === 'visible') {
                this.summaryLayerActive = false;
                await this.updateMapUnderlyingDataLayers();
            } else {
                this.summaryLayerActive = true;
                await this.updateMapUnderlyingDataLayers();
            }
        },

        /**
         * Update ui and data once tab is selected in map sidebar nav tabs
         *
         * This:
         *
         * - Listens for the selected tab in `#map-sidebar-tabs-tab-list` in
         *   `templates/dashboards/hazard.html`
         * - Updates `mapSidebarTabsDetailsTabActive` to `true` if the selected
         *   tab is the details tab, otherwise sets it to `false`.
         */
        handleMapSidebarTabsTabToggled: async function (event) {
            // Check if the 'details' tab is now active
            const selectedTabId = event?.target?.id;
            this.mapSidebarTabsDetailsTabActive = selectedTabId === 'tab-link-details';
        },

        /**
         * Update ui and data once secondary filters hazard type checkboxes are
         * checked or unchecked in bottom right map filters pane
         *
         * This:
         *
         * - Update `secondaryFilters.selectedHazardTypes` secondary filters
         * - Update data and map by calling `update`
         */
        handleSecondaryFiltersHazardTypeChecked: async function (hazardType) {
            // Collect and update selected hazard types
            const index = this.secondaryFilters.selectedHazardTypes.indexOf(hazardType);
            if (index === -1) {
                this.secondaryFilters.selectedHazardTypes.push(hazardType);
            } else {
                this.secondaryFilters.selectedHazardTypes.splice(index, 1);
            }

            // Update map and data
            await this.update();
        },

        /**
         * Update data once secondary filters population exposed type radio buttons are
         * checked.
         *
         * This:
         *
         * - Update `secondaryFilters.selectedPopulationExposed` secondary filters
         * - Update data and map by calling `update`
         */
        handleSecondaryFiltersPopulationExposedChange: async function (populationExposed) {
            // Update selected population exposed type
            this.secondaryFilters.selectedPopulationExposed = populationExposed;

            // Update map and data
            await this.update();
        },

        /**
         * Update data once secondary filters urbanicity type radio buttons are
         * checked.
         *
         * This:
         *
         * - Update `secondaryFilters.selectedUrbanicityType` secondary filters
         * - Update data and map by calling `update`
         */
        handleSecondaryFiltersUrbanicityChange: async function (urbanicityType) {
            // Update selected urbanicity type
            this.secondaryFilters.selectedUrbanicityType = urbanicityType;

            // Update map and data
            await this.update();
        },


        /**
         * Update ui and data once secondary filters are cleared in bottom right map filters pane
         *
         * This:
         *
         * - Clear or reset all secondary filters
         * - Update data and map by calling `update`
         */
        handleSecondaryFiltersCleared: async function () {
            // Reset secondary filters
            this.secondaryFilters = {
                selectedHazardTypes: [...HAZARD_TYPES],
                selectedUrbanicityType: URBANICITY_TYPE_ALL,
                selectedPopulationExposed: POPULATION_EXPOSED_PERCENT,
            };

            // Update map and data
            await this.update();
        },

        /**
         * Update ui and data once secondary filters are applied in bottom right map filters pane
         *
         * This:
         *
         * - Update all secondary filters
         * - Update data and map by calling `update`
         */
        handleSecondaryFiltersApplied: async function () {
            // Update map and data
            await this.update();
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

        // ---
        // Start: Boostrap UI methods
        // ---

        /**
         * Initialize or update bootstap UI
         */
        initBootstrapUI: async function () {
            await this.initMapSidebarTabsTabUIListener();
        },

        /**
         * Initialize event listeners for the map sidebar Bootstrap nav tabs
         * in `templates/dashboards/hazard.html`
         *
         * This method:
         * - Attaches a listener for the `'shown.bs.tab'` event on the
         *   `#map-sidebar-tabs-tab-list` element to detect when a tab becomes active.
         */
        initMapSidebarTabsTabUIListener: async function () {
            // Get the map sidebar tab list element
            const mapSidebarTabsTabList = document.getElementById('map-sidebar-tabs-tab-list');

            if (mapSidebarTabsTabList) {
                // Listen for the Bootstrap 'shown.bs.tab' event to track active tab changes
                mapSidebarTabsTabList.addEventListener('shown.bs.tab', this.handleMapSidebarTabsTabToggled);
            }
        },

        // ---
        // End: Boostrap UI methods
        // ---
        round: utils.round,
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
        await this.initBootstrapUI();
        await this.update();
    },

    /**
     * Lifecycle hook called after the component has updated its DOM tree due to a reactive state change.
     */
    updated: async function () {
        await this.initBootstrapUI();
    },
};

// Create a new Vue application instance using the HazardDash root component.
const app = Vue.createApp(HazardDash);

// Mount the `HazardDash` Vue application to the DOM element with the ID '_hazard-dash'.
app.mount('#_hazard-dash');
