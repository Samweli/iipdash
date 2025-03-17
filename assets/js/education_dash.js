import * as Vue from 'vue';
import axios from 'axios';
import Chart from 'chart.js/auto';
import maplibregl from 'maplibre-gl';
import { MaplibreLegendControl } from '@watergis/maplibre-gl-legend';
import _ from 'lodash';

import '@watergis/maplibre-gl-legend/dist/maplibre-gl-legend.css'; // direct import in CSS doesn't work

import * as settings from './conf';
import * as maps from './maps';
import * as utils from './utils';
import * as chartsConfig from './charts_config.js';

const API_ROOT = settings.API_ROOT;

const EducationDash = {
    components: {},

    data() {
        return {
            _map: null,
            _mapID: '_education-map',
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

            // institutions summary aggregations
            try {
                const institutionsAggregates = await axios.get(`${API_ROOT}education/institutions/aggregates`, {
                    params: this.lookup,
                });
                this.institutionsAggregates = institutionsAggregates.data;
            } catch (e) {
                console.log(e); // eslint-disable-line no-console
            }
        },

        initMap() {
            const map = new maplibregl.Map({
                ...maps.basemap,
                container: '_education-map',
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

            // education summary statistics by area
            const summaryLayer = _.merge({}, maps.layers['areas-education'], {
                layout: {
                    visibility: 'visible',
                },
            });

            this._map.addSource('areas-education', maps.sources['areas-education']);
            this._map.addLayer(summaryLayer);

            // education institutions
            const institutionsLayer = _.merge({}, maps.layers['education-institutions'], {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addSource('education-institutions', maps.sources['education-institutions']);
            this._map.addLayer(institutionsLayer);

            this._map.on('click', 'areas-education', (e) => {
                const countryName = this.countriesLookup[e.features[0].properties.country];
                const name = `${e.features[0].properties.name}, ${countryName}`;

                let avgDistance = utils.meters2km(e.features[0].properties.institutions_fiber_distance_avg);
                if (isNaN(avgDistance)) {
                    avgDistance = '-';
                }

                let percent10km = utils.asPercent(
                    e.features[0].properties.institutions_fiber_10km,
                    e.features[0].properties.institutions_count,
                );
                if (isNaN(percent10km)) {
                    percent10km = '-';
                }

                new maplibregl.Popup()
                    .setLngLat(e.lngLat)
                    .setHTML(
                        `<div class="card border-0" style="width: 22rem;">
                            <div class="card-header text-bg-primary">
                              <h5 class="text-white">${name}</h5>
                            </div>

                            <div class="card-body">
                                <p class="p-txt-stats-description">
                                    average distance to fiber node
                                </p>
                                <div class="d-flex flex-row align-items-center">
                                    <p class="p-txt-stats-value-primary">${avgDistance}</p>
                                    <p class="p-txt-stats-label-primary ms-1">KM</p>
                                </div>

                                <p class="p-txt-stats-description">
                                    schools within 10 km of fiber node
                                </p>
                                <div class="d-flex flex-row align-items-center">
                                    <p class="p-txt-stats-value-primary">${percent10km}</p>
                                    <p class="p-txt-stats-label-primary ms-1">%</p>
                                </div>
                            </div>
                        </div>`,
                    )
                    .addTo(this._map);
            });

            // fiber nodes
            const fiberNodesLayer = _.merge({}, maps.layers['fiber-nodes'], {
                layout: {
                    visibility: 'none',
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
                this._map.setFilter('areas-education', ['==', ['get', 'country'], this.lookup.country]);
                this._map.setFilter('education-institutions', ['==', ['get', 'country'], this.lookup.country]);
                this._map.setFilter('fiber-nodes', ['==', ['get', 'country'], this.lookup.country]);
            } else {
                this._map.setFilter('countries', null);
                this._map.setFilter('areas-education', null);
                this._map.setFilter('education-institutions', null);
                this._map.setFilter('fiber-nodes', null);
            }

            if (this.lookup.administrative_area) {
                this._map.setFilter('areas-education', ['==', ['get', 'uuid'], this.lookup.administrative_area]);
                this._map.setFilter('education-institutions', [
                    '==',
                    ['get', 'administrative_area_uuid'],
                    this.lookup.administrative_area,
                ]);
                this._map.setFilter('fiber-nodes', [
                    '==',
                    ['get', 'administrative_area_uuid'],
                    this.lookup.administrative_area,
                ]);
            }

            // pan to bounds
            if (this.lookup.administrative_area) {
                this.fitMapBounds(this.selectedRegion.properties.bbox);
            } else if (this.lookup.country) {
                this.fitMapBounds(this.selectedCountry.properties.bbox);
            }
        },

        updateCharts() {
            // Summary Fiber Optic Node Distance to schools (10, 20 & 30km)

            const schoolsFONDistanceSummaryCount = this.institutionsAggregates.fon_distances.reduce(
                (agg, record) => {
                    if (record.fon_distance_km <= 10) {
                        agg.km10 += record.count;
                    } else if (record.fon_distance_km <= 20) {
                        agg.km20 += record.count;
                    } else if (record.fon_distance_km <= 30) {
                        agg.km30 += record.count;
                    } else {
                        agg.other += record.count;
                    }

                    return agg;
                },
                { km10: 0, km20: 0, km30: 0, other: 0 },
            );

            const schoolsFONDistanceSummaryData = {
                labels: [' '], // Empty label to remove Y-axis text
                datasets: [
                    { label: '10KM', data: [schoolsFONDistanceSummaryCount.km10], backgroundColor: '#007FFF' },
                    { label: '20KM', data: [schoolsFONDistanceSummaryCount.km20], backgroundColor: '#82A5FF' },
                    { label: '30KM', data: [schoolsFONDistanceSummaryCount.km30], backgroundColor: '#BFCCFF' },
                    { label: '', data: [schoolsFONDistanceSummaryCount.other], backgroundColor: '#D9D9D9' },
                ],
            };

            const schoolsFONDistanceSummaryConfig = {
                ...chartsConfig.schoolsFONDistanceSummary,
                data: schoolsFONDistanceSummaryData,
            };

            this.clearChart(this.charts.schoolsFONDistanceSummary.id);
            const schoolsFONDistanceSummaryCtx = document
                .getElementById(this.charts.schoolsFONDistanceSummary.id)
                .getContext('2d');
            new Chart(schoolsFONDistanceSummaryCtx, schoolsFONDistanceSummaryConfig); // eslint-disable-line no-new

            // institutions fiber optic node distances

            const schoolsFONDistanceData = {
                labels: this.institutionsAggregates.fon_distances.map((record) => record.fon_distance_km),
                datasets: [
                    {
                        label: 'Number of Schools',
                        data: this.institutionsAggregates.fon_distances.map((record) => record.count),
                        backgroundColor: '#007FFF',
                        // borderRadius: 5, // Rounded bar edges for a sleek look
                        barPercentage: 0.8, // Reduce bar width
                        categoryPercentage: 0.8, // Reduce space between bars
                    },
                ],
            };

            const schoolsFONDistanceConfig = {
                ...chartsConfig.schoolsFONDistance,
                data: schoolsFONDistanceData,
            };

            this.clearChart(this.charts.schoolsFONDistance.id);
            const schoolsFONDistanceCtx = document.getElementById(this.charts.schoolsFONDistance.id).getContext('2d');
            new Chart(schoolsFONDistanceCtx, schoolsFONDistanceConfig); // eslint-disable-line no-new
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
            const summaryVisibility = this._map.getLayoutProperty('areas-education', 'visibility');
            if (summaryVisibility === 'visible') {
                this._map.setLayoutProperty('areas-education', 'visibility', 'none');
                this._map.setLayoutProperty('education-institutions', 'visibility', 'visible');
                this._map.setLayoutProperty('fiber-nodes', 'visibility', 'visible');
                this.summaryLayerActive = false;
                this.addMapLegend();
            } else {
                this._map.setLayoutProperty('education-institutions', 'visibility', 'none');
                this._map.setLayoutProperty('fiber-nodes', 'visibility', 'none');
                this._map.setLayoutProperty('areas-education', 'visibility', 'visible');
                this.summaryLayerActive = true;
                this._map.removeControl(this.legendControl);
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

        addMapLegend() {
            // TODO: use custom legend instead of this for more flexibility.
            const targets = {
                'education-institutions': 'School location',
                'fiber-nodes': 'Fiber optic node',
            };

            const legendControl = new MaplibreLegendControl(targets, {
                showDefault: true,
                onlyRendered: false,
                title: 'Active layers',
            });
            this.legendControl = Vue.markRaw(legendControl);

            this._map.addControl(this.legendControl, 'bottom-left');
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

const app = Vue.createApp(EducationDash);
app.mount('#_education-dash');
