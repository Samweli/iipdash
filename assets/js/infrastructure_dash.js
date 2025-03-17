import * as Vue from 'vue';
import axios from 'axios';
import Chart from 'chart.js/auto';
import maplibregl from 'maplibre-gl';
import _ from 'lodash';

import * as settings from './conf';
import * as maps from './maps';
import * as utils from './utils';
import * as chartsConfig from './charts_config.js';

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
            mobileCoverageAggregates: {},
            mapLoaded: false,
            summaryLayerActive: true,
            selectedCountry: null,
            selectedRegion: null,
            selectedNetworkGeneration: '3g',
            charts: {
                mobileCoverageSummary: {
                    id: 'mobile-coverage-summary-chart',
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

            // areas coverage aggregations
            try {
                const mobileCoverageAggregates = await axios.get(
                    `${API_ROOT}infrastructure/mobile-coverage/aggregates`,
                    {
                        params: this.lookup,
                    },
                );
                this.mobileCoverageAggregates = mobileCoverageAggregates.data;
            } catch (e) {
                console.log(e); // eslint-disable-line no-console
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

            // Areas coverage
            const summaryLayer3gLayer = _.merge({}, maps.layers['areas-mobile-coverage-3g'], {
                layout: {
                    visibility: 'visible',
                },
            });
            this._map.addSource('areas-mobile-coverage-3g', maps.sources['areas-mobile-coverage-3g']);
            this._map.addLayer(summaryLayer3gLayer);

            // High resolution population density
            const populationDensityHDLayer = _.merge({}, maps.layers['population-density-hd'], {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addSource('population-density-hd', maps.sources['population-density-hd']);
            this._map.addLayer(populationDensityHDLayer);

            // 3G mobile coverage
            const mobileCoverage3GLayer = _.merge({}, maps.layers['mobile-coverage-3g'], {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addSource('mobile-coverage-3g', maps.sources['mobile-coverage-3g']);
            this._map.addLayer(mobileCoverage3GLayer);

            // fiber nodes
            const fiberNodesLayer = _.merge({}, maps.layers['fiber-nodes'], {
                layout: {
                    visibility: 'visible',
                },
            });
            this._map.addSource('fiber-nodes', maps.sources['fiber-nodes']);
            this._map.addLayer(fiberNodesLayer);
        },

        updateMap: async function () {
            if (!this.mapLoaded) {
                return;
            }

            if (this.lookup.country) {
                this._map.setFilter('countries', ['==', ['get', 'country'], this.lookup.country]);
                this._map.setFilter(`areas-mobile-coverage-${this.selectedNetworkGeneration}`, [
                    '==',
                    ['get', 'country'],
                    this.lookup.country,
                ]);
                this._map.setFilter(`mobile-coverage-${this.selectedNetworkGeneration}`, [
                    '==',
                    ['get', 'country'],
                    this.lookup.country,
                ]);
                this._map.setFilter('fiber-nodes', ['==', ['get', 'country'], this.lookup.country]);
                this._map.setFilter('population-density-hd', ['==', ['get', 'country'], this.lookup.country]);
            } else {
                this._map.setFilter('countries', null);
                this._map.setFilter(`areas-mobile-coverage-${this.selectedNetworkGeneration}`, null);
                this._map.setFilter(`mobile-coverage-${this.selectedNetworkGeneration}`, null);
                this._map.setFilter('fiber-nodes', null);
                this._map.setFilter('population-density-hd', null);
            }

            if (this.lookup.administrative_area) {
                this._map.setFilter(`areas-mobile-coverage-${this.selectedNetworkGeneration}`, [
                    '==',
                    ['get', 'uuid'],
                    this.lookup.administrative_area,
                ]);
                this._map.setFilter(`mobile-coverage-${this.selectedNetworkGeneration}`, [
                    '==',
                    ['get', 'administrative_area_uuid'],
                    this.lookup.administrative_area,
                ]);
                this._map.setFilter('fiber-nodes', [
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
        },

        updateCharts() {
            // summary mobile coverage bar

            const mobileCoverageSummaryData = {
                labels: [' '], // Empty label to remove Y-axis text
                datasets: [
                    {
                        label: 'Population covered',
                        data: [this.mobileCoverageAggregates[`coverage_${this.selectedNetworkGeneration}`]],
                        backgroundColor: '#007FFF',
                    },
                    {
                        label: 'Population not covered',
                        data: [this.mobileCoverageAggregates[`no_coverage_${this.selectedNetworkGeneration}`]],
                        backgroundColor: '#D9D9D9',
                    },
                ],
            };

            const mobileCoverageSummaryConfig = {
                ...chartsConfig.mobileCoverageSummary,
                data: mobileCoverageSummaryData,
            };

            this.clearChart(this.charts.mobileCoverageSummary.id);
            const mobileCoverageSummaryCtx = document
                .getElementById(this.charts.mobileCoverageSummary.id)
                .getContext('2d');
            new Chart(mobileCoverageSummaryCtx, mobileCoverageSummaryConfig); // eslint-disable-line no-new
        },

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

        toggleSummaryLayer() {
            const summaryVisibility = this._map.getLayoutProperty(
                `areas-mobile-coverage-${this.selectedNetworkGeneration}`,
                'visibility',
            );
            if (summaryVisibility === 'visible') {
                this._map.setLayoutProperty(
                    `areas-mobile-coverage-${this.selectedNetworkGeneration}`,
                    'visibility',
                    'none',
                );
                this._map.setLayoutProperty(
                    `mobile-coverage-${this.selectedNetworkGeneration}`,
                    'visibility',
                    'visible',
                );
                this._map.setLayoutProperty('fiber-nodes', 'visibility', 'visible');
                this._map.setLayoutProperty('population-density-hd', 'visibility', 'visible');
                this.summaryLayerActive = false;
            } else {
                this._map.setLayoutProperty(`mobile-coverage-${this.selectedNetworkGeneration}`, 'visibility', 'none');
                this._map.setLayoutProperty('fiber-nodes', 'visibility', 'none');
                this._map.setLayoutProperty('population-density-hd', 'visibility', 'none');
                this._map.setLayoutProperty(
                    `areas-mobile-coverage-${this.selectedNetworkGeneration}`,
                    'visibility',
                    'visible',
                );
                this.summaryLayerActive = true;
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

        meters2km: utils.meters2km,
        asPercent: utils.asPercent,
        round: utils.round,
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
