import * as Vue from 'vue';
import axios from 'axios';
import Chart from 'chart.js/auto';
import maplibregl from 'maplibre-gl';
import _ from 'lodash';

import * as settings from './conf';
import * as maps from './maps';
import * as utils from './utils';

const API_ROOT = settings.API_ROOT;

const InfrastructureDash = {
    components: {},

    data() {
        return {
            _map: null,
            _mapID: '_infrastructure-map',
            lookup: {
                administrative_area: '',
                country: '',
            },
            countries: { features: [] },
            countriesLookup: {},
            regions: { features: [] },
            regionOptions: { features: [] },
            institutionsAggregates: { fon_distances: [] },
            mapLoaded: false,
            summaryLayerActive: true,
            legendControl: null,
            selectedCountry: null,
            selectedRegion: null,
            charts: {
                schoolsFONDistanceSummary: {
                    id: 'school-fiber-node-stats-bar-chart',
                },
                schoolsFONDistance: {
                    id: 'school-fiber-node-stats-histogram-chart',
                },
            },
        };
    },

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
    },

    methods: {
        initLookup() {},

        // initial data that won't need to be updated
        initData: async function () {
            // countries
            try {
                const countries = await axios.get(`${API_ROOT}administrative/areas`, {
                    params: { level: 1, exclude_geometry: 1 },
                });
                this.countries = countries.data;
                this.countries.features.forEach((feature) => {
                    this.countriesLookup[feature.properties.country] = feature.properties.name;
                });
            } catch (e) {
                console.log(e); // eslint-disable-line no-console
            }

            // regions
            try {
                const regions = await axios.get(`${API_ROOT}administrative/areas`, {
                    params: { level: 2, exclude_geometry: 1 },
                });
                this.regions = regions.data;
                this.regionOptions = _.cloneDeep(this.regions);
            } catch (e) {
                console.log(e); // eslint-disable-line no-console
            }
        },

        updateData: async function () {
            if (this.lookup.country) {
                this.selectedCountry = _.find(this.countries.features, ['properties.country', this.lookup.country]);
            }

            if (this.lookup.administrative_area) {
                this.selectedRegion = _.find(this.regions.features, { id: this.lookup.administrative_area });
            }
        },

        initMap() {
            const map = new maplibregl.Map({
                ...maps.basemap,
                container: this._mapID,
            });

            this._map = Vue.markRaw(map);

            this._map.on('load', () => {
                this.mapLoaded = true;
                this.addMapLayers();
            });

            const navigationControl = new maplibregl.NavigationControl({
                visualizePitch: true,
                visualizeRoll: true,
                showZoom: true,
                showCompass: true,
            });
            map.addControl(navigationControl);
        },

        addMapLayers: async function () {
            // country boundaries
            this._map.addSource('countries', maps.sources.countries);
            this._map.addLayer(maps.layers.countries);

            // fiber nodes
            const fiberNodesLayer = _.merge({}, maps.layers['fiber-nodes'], {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addSource('fiber-nodes', maps.sources['fiber-nodes']);
            this._map.addLayer(fiberNodesLayer);
        },

        updateMap: async function () {},

        updateCharts() {},

        update: async function () {
            try {
                await this.updateData();
            } catch (e) {
                console.log(e); // eslint-disable-line no-console
            }

            this.updateMap();
            this.updateCharts();

            const event = new Event('page-updated');
            window.dispatchEvent(event);
        },

        updateCountry() {
            this.lookup.administrative_area = null;

            if (this.lookup.country) {
                this.regionOptions.features = _.filter(this.regions.features, [
                    'properties.country',
                    this.lookup.country,
                ]);
            } else {
                this.regionOptions.features = _.cloneDeep(this.regions.features);
            }

            this.update();
        },

        toggleSummaryLayer() {},

        clearChart(elementID) {
            const ctx = document.getElementById(elementID);

            try {
                Chart.getChart(ctx).destroy();
            } catch (e) {
                // chart didn't exist yet
            }
        },

        meters2km: utils.meters2km,
        asPercent: utils.asPercent,
    },

    mounted() {
        this.initLookup();
        this.initData();
        this.initMap();
        this.update();
    },
};

const app = Vue.createApp(InfrastructureDash);
app.mount('#_infrastructure-dash');
