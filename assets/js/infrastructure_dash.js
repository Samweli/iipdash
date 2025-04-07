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
            regionsMobileCoverage: { features: [] },
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
                regionsMobileCoverage: {
                    id: 'regions-mobile-coverage-chart',
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

        summaryCSVDownloadURL() {
            const params = {
                country: this.lookup.country,
                uuid: this.lookup.administrative_area,
                level: 3,
            };
            return utils.updateURLParams(`${API_ROOT}administrative/areas-mobile-coverage/download`, params);
        },
    },

    methods: {
        initLookup() {},

        // initial data that won't need to be updated
        initData: async function () {
            // countries
            try {
                const countries = await axios.get(`${API_ROOT}administrative/areas`, {
                    params: { level: 2, exclude_geometry: 1 },
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
                    params: { level: 3, exclude_geometry: 1 },
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

            // coverage per region
            try {
                const regionsMobileCoverage = await axios.get(`${API_ROOT}administrative/areas-mobile-coverage/`, {
                    params: {
                        country: this.lookup.country || '',
                        administrative_area_level: 3,
                        exclude_geometry: true,
                    },
                });
                this.regionsMobileCoverage = regionsMobileCoverage.data;
            } catch (e) {
                console.log(e); // eslint-disable-line no-console
            }

            // areas coverage aggregations
            try {
                const mobileCoverageAggregates = await axios.get(
                    `${API_ROOT}infrastructure/mobile-coverage/aggregates`,
                    {
                        params: { ...this.lookup, administrative_area_level: 3 },
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
            const mapSources = await maps.getSources();

            // country boundaries
            this._map.addSource('countries', mapSources.countries);
            this._map.addLayer(maps.layers.countries);

            // Areas coverage
            this._map.addSource('areas-mobile-coverage', mapSources['areas-mobile-coverage']);

            const summaryLayer3gLayer = _.merge({}, maps.layers['areas-mobile-coverage-3g'], {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addLayer(summaryLayer3gLayer);

            const summaryLayer4gLayer = _.merge({}, maps.layers['areas-mobile-coverage-4g'], {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addLayer(summaryLayer4gLayer);

            this.updateMobileCoverageSummaryLayer();

            // regions boundaries
            const regionsLayer = _.merge({}, maps.layers.regions, {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addSource('regions', mapSources.regions);
            this._map.addLayer(regionsLayer);

            // High resolution population density
            const populationDensityHDLayer = _.merge({}, maps.layers['population-density-hd'], {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addSource('population-density-hd', mapSources['population-density-hd']);
            this._map.addLayer(populationDensityHDLayer);

            // 3G mobile coverage
            const mobileCoverage3GLayer = _.merge({}, maps.layers['mobile-coverage-3g'], {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addSource('mobile-coverage-3g', mapSources['mobile-coverage-3g']);
            this._map.addLayer(mobileCoverage3GLayer);

            // 4G mobile coverage
            const mobileCoverage4GLayer = _.merge({}, maps.layers['mobile-coverage-4g'], {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addSource('mobile-coverage-4g', mapSources['mobile-coverage-4g']);
            this._map.addLayer(mobileCoverage4GLayer);

            this._map.on('click', 'areas-mobile-coverage-3g', this.showSummaryMapPopup);
            this._map.on('click', 'areas-mobile-coverage-4g', this.showSummaryMapPopup);
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
                this._map.setFilter('population-density-hd', ['==', ['get', 'country'], this.lookup.country]);
            } else {
                this._map.setFilter('countries', null);
                this._map.setFilter(`areas-mobile-coverage-${this.selectedNetworkGeneration}`, null);
                this._map.setFilter('population-density-hd', null);
            }

            if (this.lookup.administrative_area) {
                this._map.setFilter(`areas-mobile-coverage-${this.selectedNetworkGeneration}`, [
                    '==',
                    ['get', 'uuid'],
                    this.lookup.administrative_area,
                ]);
                this._map.setFilter('population-density-hd', [
                    '==',
                    ['get', 'administrative_area_uuid'],
                    this.lookup.administrative_area,
                ]);
            }

            this.updateMobileCoverageLayer();
            this.updateMobileCoverageSummaryLayer();

            // highlight selected region
            if (this.lookup.administrative_area) {
                this._map.setFilter('regions', ['==', ['get', 'uuid'], this.lookup.administrative_area]);
                this._map.setLayoutProperty('regions', 'visibility', 'visible');
            } else {
                this._map.setLayoutProperty('regions', 'visibility', 'none');
                this._map.setFilter('regions', null);
            }

            // highlight selected country
            if (this.lookup.country) {
                this._map.setFilter('countries', ['==', ['get', 'country'], this.lookup.country]);
            } else {
                this._map.setFilter('countries', null);
            }

            // pan to bounds
            if (this.lookup.administrative_area) {
                this.fitMapBounds(this.selectedRegion.properties.bbox);
            } else if (this.lookup.country) {
                this.fitMapBounds(this.selectedCountry.properties.bbox);
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

            // regions mobile coverage
            const regionsMobileCoverageData = {
                datasets: [
                    {
                        label: '',
                        data: this.regionsMobileCoverage.features.map((coverage) => {
                            return {
                                x: this.round(coverage.properties.population_density_hd_avg, 2),
                                y: this.round(coverage.properties[`coverage_${this.selectedNetworkGeneration}`], 2),
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

            const regionsMobileCoverageConfig = {
                ...chartsConfig.regionsMobileCoverage,
                data: regionsMobileCoverageData,
            };

            this.clearChart(this.charts.regionsMobileCoverage.id);
            const regionsMobileCoverageCtx = document
                .getElementById(this.charts.regionsMobileCoverage.id)
                .getContext('2d');
            new Chart(regionsMobileCoverageCtx, regionsMobileCoverageConfig); // eslint-disable-line no-new
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
                this._map.setLayoutProperty('population-density-hd', 'visibility', 'visible');
                this.summaryLayerActive = false;
                this.updateMobileCoverageLayer();
            } else {
                this._map.setLayoutProperty(`mobile-coverage-${this.selectedNetworkGeneration}`, 'visibility', 'none');
                this._map.setLayoutProperty('population-density-hd', 'visibility', 'none');
                this._map.setLayoutProperty(
                    `areas-mobile-coverage-${this.selectedNetworkGeneration}`,
                    'visibility',
                    'visible',
                );
                this.summaryLayerActive = true;
            }
        },

        updateMobileCoverageSummaryLayer: async function () {
            if (!this.summaryLayerActive) {
                return;
            }

            if (this.selectedNetworkGeneration === '4g') {
                this._map.setLayoutProperty('areas-mobile-coverage-3g', 'visibility', 'none');
                this._map.setLayoutProperty('areas-mobile-coverage-4g', 'visibility', 'visible');
            } else {
                this._map.setLayoutProperty('areas-mobile-coverage-4g', 'visibility', 'none');
                this._map.setLayoutProperty('areas-mobile-coverage-3g', 'visibility', 'visible');
            }
        },

        updateMobileCoverageLayer: async function () {
            if (this.summaryLayerActive) {
                return;
            }

            const tilesLookup = { network_generation_code: this.selectedNetworkGeneration };

            if (this.lookup.country && !this.lookup.administrative_area) {
                tilesLookup.administrative_area = this.selectedCountry.id;
            } else if (this.lookup.administrative_area) {
                tilesLookup.administrative_area = this.selectedRegion.id;
            } else {
                tilesLookup.administrative_area_level = 1;
            }

            const tilesURLs = await maps.getMobileCoverageTMSURLs(tilesLookup);
            this._map.getSource(`mobile-coverage-${this.selectedNetworkGeneration}`).setTiles(tilesURLs);

            if (this.selectedNetworkGeneration === '4g') {
                this._map.setLayoutProperty('mobile-coverage-3g', 'visibility', 'none');
                this._map.setLayoutProperty('mobile-coverage-4g', 'visibility', 'visible');
            } else {
                this._map.setLayoutProperty('mobile-coverage-4g', 'visibility', 'none');
                this._map.setLayoutProperty('mobile-coverage-3g', 'visibility', 'visible');
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

        fitMapBounds(bbox, options = {}) {
            this._map.fitBounds(
                [
                    [bbox[0], bbox[1]],
                    [bbox[2], bbox[3]],
                ],
                options,
            );
        },

        showSummaryMapPopup(e) {
            const countryName = this.countriesLookup[e.features[0].properties.country];
            const name = `${e.features[0].properties.name}, ${countryName}`;

            let coverage3G = this.round(e.features[0].properties.coverage_3g);
            if (isNaN(coverage3G)) {
                coverage3G = '-';
            }

            let coverage4G = this.round(e.features[0].properties.coverage_4g);
            if (isNaN(coverage4G)) {
                coverage4G = '-';
            }

            new maplibregl.Popup()
                .setLngLat(e.lngLat)
                .setHTML(
                    `<div class="card border-0">
                        <div class="card-header text-bg-primary">
                          <h5 class="text-white pe-3">${name}</h5>
                        </div>

                        <div class="card-body">
                            <p class="p-txt-stats-description">
                                covered population <strong>(3G)</strong>
                            </p>
                            <div class="d-flex flex-row align-items-center">
                                <p class="p-txt-stats-value-primary">${coverage3G} %</p>
                            </div>

                            <p class="p-txt-stats-description">
                                covered population <strong>(4G)</strong>
                            </p>
                            <div class="d-flex flex-row align-items-center">
                                <p class="p-txt-stats-value-primary">${coverage4G} %</p>
                            </div>
                        </div>
                    </div>`,
                )
                .addTo(this._map);
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
