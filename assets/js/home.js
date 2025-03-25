import * as bootstrap from 'bootstrap';
import * as Vue from 'vue';
import maplibregl from 'maplibre-gl';

import * as maps from './maps';
import { fetchCatalogCategories, fetchCatalogLayers } from './api';

/**
 *  HomeDash Vue application.
 */
const HomeDash = {
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
            _mapId: 'home-map',
            mapLoaded: false,
            catalogCategories: [],
            catalogLayers: [],
        };
    },

    /**
     * Defines computed properties derived from the component's data.
     */
    computed: {},

    /**
     * Defines methods that handle user interactions and component logic.
     */
    methods: {
        /**
         * Load initial data.
         *
         * This loads:
         * - Catalog categories
         * - Catalog layers
         */
        initData: async function () {
            const [catalogCategories, catalogLayers] = await Promise.all([
                fetchCatalogCategories(),
                fetchCatalogLayers(),
            ]);
            this.catalogCategories = catalogCategories;
            this.catalogLayers = catalogLayers;
        },

        /**
         * Update data.
         */
        updateData: async function () {},

        /**
         * Initalize `maplibregl.Map` and load layers.
         */
        initMap: async function () {
            const map = new maplibregl.Map({
                ...maps.basemap,
                container: this._mapId,
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

        /**
         * Add map layers.
         */
        addMapLayers: async function () {
            // country boundaries
            this._map.addSource(maps.layers.countries.id, maps.sources.countries);
            this._map.addLayer(maps.layers.countries);
        },

        /**
         * Add map layers legend.
         */
        addMapLegend: async function () {},

        /**
         * Toggle (set or unset) map filters
         */
        toggleMapFilters: async function () {},

        /**
         * Toggle map layers
         */
        toggleMapLayers: async function () {},

        /**
         * Update (set filters, unset filters) map.
         */
        updateMap: async function () {
            if (!this.mapLoaded) {
                return;
            }

            try {
                // toggle map filters
                await this.toggleMapFilters();
                // toggle layers
                await this.toggleMapLayers();
            } catch (e) {
                console.log(e); // eslint-disable-line no-console
            }
        },

        /**
         * Update data and map.
         */
        update: async function () {
            try {
                await this.updateData();
            } catch (e) {
                console.log(e); // eslint-disable-line no-console
            }

            this.updateMap();

            const event = new Event('page-updated');
            window.dispatchEvent(event);
        },

        initBootstrapUI: async function () {
            // Init layers popovers
            const layerItemPopoverTemplate = document.querySelector('#layer-item-popover-template').innerHTML;
            document.querySelectorAll('.popover-trigger').forEach((el) => {
                const popoverContentId = el.getAttribute('data-popover-content');
                const popoverContent = document.querySelector(popoverContentId).innerHTML;
                return new bootstrap.Popover(el, {
                    html: true,
                    content: popoverContent,
                    placement: 'auto',
                    template: layerItemPopoverTemplate,
                });
            });
        },
    },

    /**
     * Lifecycle hook called after the component has been mounted to the DOM.
     */
    mounted: async function () {
        await this.initData();
        await this.initMap();
        await this.initBootstrapUI();
        await this.update();
    },
};

// Create a new Vue application instance using the HomeDash root component.
const app = Vue.createApp(HomeDash);

// Mount the `HomeDash` Vue application to the DOM element with the ID 'home'.
app.mount('#home');
