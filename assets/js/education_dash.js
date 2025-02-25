import * as Vue from 'vue';
import axios from 'axios';
import maplibregl from 'maplibre-gl';
import { MaplibreLegendControl } from '@watergis/maplibre-gl-legend';
import _ from 'lodash';

import '@watergis/maplibre-gl-legend/dist/maplibre-gl-legend.css'; // direct import in CSS doesn't work

import * as settings from './conf';
import * as maps from './maps';

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
            regions: { features: [] },
            regionOptions: { features: [] },
            mapLoaded: false,
            summaryLayerActive: true,
        };
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

        updateData: async function () {},

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

            // fiber nodes
            const fiberNodesLayer = _.merge({}, maps.layers['fiber-nodes'], {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addSource('fiber-nodes', maps.sources['fiber-nodes']);
            this._map.addLayer(fiberNodesLayer);

            // Legend
            const targets = {
                'education-institutions': 'School location',
                'fiber-nodes': 'Fiber optic node',
            };

            this._map.addControl(
                new MaplibreLegendControl(targets, {
                    showDefault: true,
                    onlyRendered: false,
                    title: 'Active layers',
                }),
                'bottom-left',
            );
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
        },

        update: async function () {
            try {
                await this.updateData();
                this.updateMap();
            } catch (e) {
                console.log(e); // eslint-disable-line no-console
            }

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
            } else {
                this._map.setLayoutProperty('education-institutions', 'visibility', 'none');
                this._map.setLayoutProperty('fiber-nodes', 'visibility', 'none');
                this._map.setLayoutProperty('areas-education', 'visibility', 'visible');
                this.summaryLayerActive = true;
            }
        },
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
