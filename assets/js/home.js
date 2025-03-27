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
            catalogSelectedCategories: [],
            catalogSelectedLayers: [],
            catalogLayerSearchTerm: '',
        };
    },

    /**
     * Defines computed properties derived from the component's data.
     */
    computed: {
        // Filtered catalog layers based on search term and selected catalog categories
        catalogFilteredLayers() {
            return this.catalogLayers.filter((layer) => {
                // TODO: throttle
                const matchesCatalogLayerSearch = layer?.name
                    .toLowerCase()
                    .includes(this.catalogLayerSearchTerm.toLowerCase());
                const matchesCatalogCategory =
                    this.catalogSelectedCategories?.length === 0 ||
                    this.catalogSelectedCategories?.includes(layer?.category.uuid);
                return matchesCatalogLayerSearch && matchesCatalogCategory;
            });
        },
    },

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
            this.catalogCategories = catalogCategories.map((category) => {
                const activeClass = `layers-category-${category.code}-pill`;
                return { ...category, activeClass };
            });
            this.catalogLayers = catalogLayers.map((layer) => {
                const category = layer?.categories?.[0] || null;
                if (category) {
                    category.activeClass = `layers-category-${category.code}-pill`;
                }
                const dataPopoverContent = `#layer-item-${layer.uuid}-popover-content`;
                return { ...layer, dataPopoverContent, category };
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
         * Update data.
         */
        updateData: async function () {},

        /**
         * Update (set filters, unset filters) map.
         */
        updateMap: async function () {
            if (!this.mapLoaded) {
                return;
            }

            // toggle map filters
            await this.toggleMapFilters();
            // toggle layers
            await this.toggleMapLayers();
        },

        /**
         * Update data and map.
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

        // Start: UI event handlers

        /**
         * Clear layers category filter once clear button clicked
         */
        handleClearCatalogLayersCategoryFilter: async function () {
            this.catalogSelectedCategories = [];
            await this.closeCatalogLayersCategoryFilterDropdownUI();
            // TODO: update map & ui
        },

        /**
         * Apply layers category filter once apply button clicked
         */
        handleApplyCatalogLayersCategoryFilter: async function () {
            await this.closeCatalogLayersCategoryFilterDropdownUI();
            // TODO: update map & ui
        },

        /**
         * Handle catalog layer checked once a checkbox checked or unchecked
         */
        handleCatalogLayerChecked: async function (catalogLayer) {
            const index = this.catalogSelectedLayers.indexOf(catalogLayer.uuid);
            if (index === -1) {
                this.catalogSelectedLayers.push(catalogLayer.uuid);
            } else {
                this.catalogSelectedLayers.splice(index, 1);
            }
            // TODO: handle selected/unselected layer
            // TODO: update map & ui
            // TODO: await this.update()
        },

        // End: UI event handlers

        // Start: Boostrap UI

        initBootstrapUI: async function () {
            // Init layer item popovers ui
            await this.initLayerItemPopoversUI();
            // TODO: init other bootstrap uis
        },

        /**
         * Setup layer item popovers.
         */
        initLayerItemPopoversUI: async function () {
            const layerItemPopoverTemplate = document.querySelector('#layer-item-popover-template')?.innerHTML;
            document.querySelectorAll('.popover-trigger').forEach((el) => {
                const layerItemPopoverContentId = el.getAttribute('data-popover-content');
                const layerItemPopoverContent = document.querySelector(layerItemPopoverContentId)?.innerHTML;
                if (layerItemPopoverTemplate && layerItemPopoverContent) {
                    // eslint-disable-next-line no-new
                    new bootstrap.Popover(el, {
                        html: true,
                        content: layerItemPopoverContent,
                        placement: 'auto',
                        template: layerItemPopoverTemplate,
                    });
                }
            });
        },

        /**
         * Close layers category filter dropdown menu
         */
        closeCatalogLayersCategoryFilterDropdownUI: async function () {
            const layersCategoryFilterDropdownEl = document.getElementById('layers-category-filter-dropdown');
            if (layersCategoryFilterDropdownEl) {
                const instance = bootstrap.Dropdown.getOrCreateInstance(layersCategoryFilterDropdownEl);
                instance.hide();
            }
        },

        // End: Boostrap UI
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

    /**
     * Lifecycle hook called after the component has updated its DOM tree due to a reactive state change.
     */
    updated: async function () {
        await this.initBootstrapUI();
    },
};

// Create a new Vue application instance using the HomeDash root component.
const app = Vue.createApp(HomeDash);

// Mount the `HomeDash` Vue application to the DOM element with the ID 'home'.
app.mount('#home');
