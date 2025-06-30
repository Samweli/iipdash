import * as Vue from 'vue';

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
        };
    },

    /**
     * Defines computed properties derived from the component's data.
     */
    computed: {},

    /**
     * Defines methods that handle user interactions and component logic.
     */
    methods: {},

    /**
     * Lifecycle hook called after the component has been mounted to the DOM.
     */
    mounted: async function () {},

    /**
     * Lifecycle hook called after the component has updated its DOM tree due to a reactive state change.
     */
    updated: async function () {},
};

// Create a new Vue application instance using the HazardDash root component.
const app = Vue.createApp(HazardDash);

// Mount the `HazardDash` Vue application to the DOM element with the ID '_hazard-dash'.
app.mount('#_hazard-dash');
