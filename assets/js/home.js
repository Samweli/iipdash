import _ from 'lodash';
import * as bootstrap from 'bootstrap';
import * as Vue from 'vue';
import maplibregl from 'maplibre-gl';

import * as settings from './conf';
import * as maps from './maps';
import { fetchCatalogCategories, fetchCatalogLayers, fetchCountries, fetchRegions } from './api';

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
            lookup: {
                administrative_area: '',
                country: '',
            },
            catalogCategories: [],
            catalogLayers: [],
            catalogSelectedCategories: [],
            catalogSelectedLayers: [],
            catalogLayerSearchTerm: '',
            countries: { features: [] },
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
         * - Countries
         * - Regions
         */
        initData: async function () {
            const [catalogCategories, catalogLayers, countries, regions] = await Promise.all([
                fetchCatalogCategories(),
                fetchCatalogLayers(),
                fetchCountries(),
                fetchRegions(),
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
            this.countries = countries;
            this.regions = _.cloneDeep(regions);
            this.regionOptions = _.cloneDeep(regions);
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
            // country boundaries layer
            this._map.addSource(maps.layers.countries.id, maps.sources.countries);
            this._map.addLayer(maps.layers.countries);

            // regions boundaries layer
            const regionsLayer = _.merge({}, maps.layers.regions, {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addSource('regions', maps.sources.regions);
            this._map.addLayer(regionsLayer);

            // High resolution population density
            const populationDensityHDLayer = _.merge({}, maps.layers['population-density-hd'], {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addSource('population-density-hd', maps.sources['population-density-hd']);
            this._map.addLayer(populationDensityHDLayer);

            // Education institutions layer
            const educationInstitutionsLayer = _.merge({}, maps.layers['education-institutions'], {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addSource('education-institutions', maps.sources['education-institutions']);
            this._map.addLayer(educationInstitutionsLayer);

            // Health care facilities layer
            const healthFacilitiesLayer = _.merge({}, maps.layers['health-facilities'], {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addSource('health-facilities', maps.sources['health-facilities']);
            this._map.addLayer(healthFacilitiesLayer);

            // Fiber nodes layer
            const fiberNodesLayer = _.merge({}, maps.layers['fiber-nodes'], {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addSource('fiber-nodes', maps.sources['fiber-nodes']);
            this._map.addLayer(fiberNodesLayer);

            // Cell towers layer
            const cellTowersLayer = _.merge({}, maps.layers['cell-towers'], {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addSource('cell-towers', maps.sources['cell-towers']);
            this._map.addLayer(cellTowersLayer);

            // 3G mobile coverage layer
            const mobileCoverage3GLayer = _.merge({}, maps.layers['mobile-coverage-3g'], {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addSource('mobile-coverage-3g', maps.sources['mobile-coverage-3g']);
            this._map.addLayer(mobileCoverage3GLayer);

            // 4G mobile coverage layer
            const mobileCoverage4GLayer = _.merge({}, maps.layers['mobile-coverage-4g'], {
                layout: {
                    visibility: 'none',
                },
            });
            this._map.addSource('mobile-coverage-4g', maps.sources['mobile-coverage-4g']);
            this._map.addLayer(mobileCoverage4GLayer);
        },

        /**
         * Add map layers legend.
         */
        addMapLegend: async function () {},

        /**
         * Update data.
         *
         * This:
         * - Set current selected country
         * - Set current selected region
         */
        updateData: async function () {
            // Update selected region
            if (this.lookup.country) {
                this.selectedCountry = _.find(this.countries.features, ['properties.country', this.lookup.country]);
            }

            // Update selected country
            if (this.lookup.administrative_area) {
                this.selectedRegion = _.find(this.regions.features, { id: this.lookup.administrative_area });
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
         * Update (set or unset) map filters and visibilities to control catalog layers.
         *
         * Controlled catalog layers are:
         *
         * - `education-institutions`
         * - `health-facilities`
         * - `fiber-nodes`
         * - `cell-towers`
         * - `mobile-coverage-3g`
         * - `mobile-coverage-4g`
         *
         * This:
         *
         * - Filter catalog layers based on current selected `country` and `region`
         * - Toggle catalog layer visibility based on current selected catalog layers, if any exists in `catalogSelectedLayers`
         */
        updateMapCatalogLayers: async function () {
            // 1. Filter catalog layers based on current selected `country` and `region`

            // 1.0 Lookup for mobile coverage layers i.e `mobile-coverage-3g` or `mobile-coverage-4g`
            const mobileCoverageTilesLookup = {};

            // 1.1 Filter catalog layers based on current selected `country`
            if (this.lookup.country) {
                this._map.setFilter('population-density-hd', ['==', ['get', 'country'], this.lookup.country]);
                this._map.setFilter('education-institutions', ['==', ['get', 'country'], this.lookup.country]);
                this._map.setFilter('health-facilities', ['==', ['get', 'country'], this.lookup.country]);
                this._map.setFilter('fiber-nodes', ['==', ['get', 'country'], this.lookup.country]);
                this._map.setFilter('cell-towers', ['==', ['get', 'country'], this.lookup.country]);
                mobileCoverageTilesLookup.administrative_area = this.selectedCountry.id;
            } else {
                this._map.setFilter('population-density-hd', null);
                this._map.setFilter('education-institutions', null);
                this._map.setFilter('health-facilities', null);
                this._map.setFilter('fiber-nodes', null);
                this._map.setFilter('cell-towers', null);
            }

            // 1.2 Filter catalog layers based on current selected `region`
            if (this.lookup.administrative_area) {
                this._map.setFilter('population-density-hd', [
                    '==',
                    ['get', 'administrative_area_uuid'],
                    this.lookup.administrative_area,
                ]);
                this._map.setFilter('education-institutions', [
                    '==',
                    ['get', 'administrative_area_uuid'],
                    this.lookup.administrative_area,
                ]);
                this._map.setFilter('health-facilities', [
                    '==',
                    ['get', 'administrative_area_uuid'],
                    this.lookup.administrative_area,
                ]);
                this._map.setFilter('fiber-nodes', [
                    '==',
                    ['get', 'administrative_area_uuid'],
                    this.lookup.administrative_area,
                ]);
                this._map.setFilter('cell-towers', [
                    '==',
                    ['get', 'administrative_area_uuid'],
                    this.lookup.administrative_area,
                ]);
                mobileCoverageTilesLookup.administrative_area = this.selectedRegion.id;
            }

            // 1.3 Filter mobile coverage layers i.e `mobile-coverage-3g` or `mobile-coverage-4g`
            // based on current selected `country` and `region`
            if (!this.lookup.country && !this.lookup.administrative_area) {
                mobileCoverageTilesLookup.administrative_area_level = settings.ADMINISTRATIVE_AREA_ALL_COUNTRIES_LEVEL;
                delete mobileCoverageTilesLookup.administrative_area;
            }

            // 1.3.1 Filter `mobile-coverage-3g` based on current selected `country` and `region`
            if (this.catalogSelectedLayers.includes('mobile-coverage-3g')) {
                const mobileCoverage3gTilesLookup = _.merge({}, mobileCoverageTilesLookup, {
                    network_generation_code: '3g',
                });
                const mobileCoverage3gTilesURLs = await maps.getMobileCoverageTMSURLs(mobileCoverage3gTilesLookup);
                this._map.getSource('mobile-coverage-3g').setTiles(mobileCoverage3gTilesURLs);
            }

            // 1.3.2 Filter `mobile-coverage-4g` based on current selected `country` and `region`
            if (this.catalogSelectedLayers.includes('mobile-coverage-4g')) {
                const mobileCoverage4gTilesLookup = _.merge({}, mobileCoverageTilesLookup, {
                    network_generation_code: '4g',
                });
                const mobileCoverage4gTilesURLs = await maps.getMobileCoverageTMSURLs(mobileCoverage4gTilesLookup);
                this._map.getSource('mobile-coverage-4g').setTiles(mobileCoverage4gTilesURLs);
            }

            // 2. Toggle catalog layer visibility based on current selected catalog layers
            // if any exists in `catalogSelectedLayers`

            // 2.1 There are `catalogSelectedLayers`, show only selected catalog layers
            if (this.catalogSelectedLayers && this.catalogSelectedLayers.length >= 1) {
                // 2.1.1 Toggle `population-density-hd` layer visibility
                const showPopulationDensityHDLayer = this.catalogSelectedLayers.includes('population-density-hd');
                if (showPopulationDensityHDLayer) {
                    this._map.setLayoutProperty('population-density-hd', 'visibility', 'visible');
                } else {
                    this._map.setLayoutProperty('population-density-hd', 'visibility', 'none');
                }

                // 2.1.2 Toggle `education-institutions` layer visibility
                const showEducationInstitutionsLayer = this.catalogSelectedLayers.includes('education-institutions');
                if (showEducationInstitutionsLayer) {
                    this._map.setLayoutProperty('education-institutions', 'visibility', 'visible');
                } else {
                    this._map.setLayoutProperty('education-institutions', 'visibility', 'none');
                }

                // 2.1.3 Toggle `health-facilities` layer visibility
                const showHealthFacilitiesLayer = this.catalogSelectedLayers.includes('health-facilities');
                if (showHealthFacilitiesLayer) {
                    this._map.setLayoutProperty('health-facilities', 'visibility', 'visible');
                } else {
                    this._map.setLayoutProperty('health-facilities', 'visibility', 'none');
                }

                // 2.1.4 Toggle `fiber-nodes` layer visibility
                const showFiberNodesLayer = this.catalogSelectedLayers.includes('fiber-nodes');
                if (showFiberNodesLayer) {
                    this._map.setLayoutProperty('fiber-nodes', 'visibility', 'visible');
                } else {
                    this._map.setLayoutProperty('fiber-nodes', 'visibility', 'none');
                }

                // 2.1.5 Toggle `cell-towers` layer visibility
                const showCellTowersLayer = this.catalogSelectedLayers.includes('cell-towers');
                if (showCellTowersLayer) {
                    this._map.setLayoutProperty('cell-towers', 'visibility', 'visible');
                } else {
                    this._map.setLayoutProperty('cell-towers', 'visibility', 'none');
                }

                // 2.1.6 Toggle `mobile-coverage-3g` layer visibility
                const showMobileCoverage3GLayer = this.catalogSelectedLayers.includes('mobile-coverage-3g');
                if (showMobileCoverage3GLayer) {
                    this._map.setLayoutProperty('mobile-coverage-3g', 'visibility', 'visible');
                } else {
                    this._map.setLayoutProperty('mobile-coverage-3g', 'visibility', 'none');
                }

                // 2.1.7 Toggle `mobile-coverage-4g` layer visibility
                const showMobileCoverage4GLayer = this.catalogSelectedLayers.includes('mobile-coverage-4g');
                if (showMobileCoverage4GLayer) {
                    this._map.setLayoutProperty('mobile-coverage-4g', 'visibility', 'visible');
                } else {
                    this._map.setLayoutProperty('mobile-coverage-4g', 'visibility', 'none');
                }
            }

            // 2.2 No `catalogSelectedLayers`, hide all catalog layers always
            else {
                this._map.setLayoutProperty('population-density-hd', 'visibility', 'none');
                this._map.setLayoutProperty('education-institutions', 'visibility', 'none');
                this._map.setLayoutProperty('health-facilities', 'visibility', 'none');
                this._map.setLayoutProperty('fiber-nodes', 'visibility', 'none');
                this._map.setLayoutProperty('cell-towers', 'visibility', 'none');
                this._map.setLayoutProperty('mobile-coverage-3g', 'visibility', 'none');
                this._map.setLayoutProperty('mobile-coverage-4g', 'visibility', 'none');
            }
        },

        /**
         * Update map to fit the bounds
         *
         * This pans and zooms the map to contain its visible area within the specified geographical bounding box.
         *
         * This:
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
                this._map.fitBounds(
                    [
                        [bbox[0], bbox[1]],
                        [bbox[2], bbox[3]],
                    ],
                    options,
                );
            }

            // Restore exact map zoom and center
            else {
                this._map.flyTo({
                    center: settings.MAP_DEFAULT_CENTER,
                    zoom: settings.MAP_DEFAULT_ZOOM,
                });
            }
        },

        /**
         * Update (set filters, unset filters) map.
         */
        updateMap: async function () {
            if (!this.mapLoaded) {
                return;
            }

            // filter, toggle visibility of map layers
            await this.updateMapCatalogLayers();
            await this.updateMapAdministrativeBoundaryLayers();

            // fit map to bound
            await this.updateMapFitBounds();
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
         * Update ui and data once country selected in top map pane country selection
         *
         * This:
         * - Update regionOptions
         * - Update data and map by calling `update`
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
        },

        /**
         * Update ui and data once region selected in top map pane country selection
         *
         * This:
         * - Update data and map by calling `update`
         */
        handleRegionSelected: async function () {
            await this.update();
        },

        /**
         * Clear layers category filter once clear button clicked
         */
        handleClearCatalogLayersCategoryFilter: async function () {
            this.catalogSelectedCategories = [];
            await this.closeCatalogLayersCategoryFilterDropdownUI();
        },

        /**
         * Apply layers category filter once apply button clicked
         */
        handleApplyCatalogLayersCategoryFilter: async function () {
            await this.closeCatalogLayersCategoryFilterDropdownUI();
        },

        /**
         * Handle catalog layer checked once a checkbox checked or unchecked
         */
        handleCatalogLayerChecked: async function (catalogLayer) {
            // Collect and update catalog selected layers
            const index = this.catalogSelectedLayers.indexOf(catalogLayer.code);
            if (index === -1) {
                this.catalogSelectedLayers.push(catalogLayer.code);
            } else {
                this.catalogSelectedLayers.splice(index, 1);
            }

            // Update map & data
            await this.update();
        },

        // End: UI event handlers

        // Start: Boostrap UI

        /**
         * Initialize or update bootstap UI
         */
        initBootstrapUI: async function () {
            // Init layer item popovers ui
            await this.initLayerItemPopoversUI();
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
