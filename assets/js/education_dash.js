import * as Vue from 'vue';
import axios from 'axios';
import maplibregl from 'maplibre-gl';

import * as settings from './conf';
import * as maps from './maps';


const EducationDash = {
    components: {},

    data () {
        return {
            _map: null,
            _mapID: '_education-map',
            lookup: {},
            results: {features: []}
        }
    },

    methods: {

        initLookup () {},

        updateData: async function () {},

        initMap () {
            const map = new maplibregl.Map({
                ...maps.basemap,
                container: '_education-map'
            });

            const navigationControl = new maplibregl.NavigationControl({
                visualizePitch: true,
                visualizeRoll: true,
                showZoom: true,
                showCompass: true
            });
            map.addControl(navigationControl);

            this._map = Vue.markRaw(map);

        },

        updateMap: async function () {
            this._map.on('load', () => {

                // education summary statistics by area
                this._map.addSource('areas-education', maps.sources['areas-education']);
                this._map.addLayer(maps.layers['areas-education']);
            });
       },

        update: async function () {
            try {
                await this.updateData();
                this.updateMap();
            } catch (e) {
                console.log(e)
            }

            const event = new Event('page-updated');
            window.dispatchEvent(event);
        },
    },

    mounted () {
        this.initLookup();
        this.initMap();
        this.update();
    }
}

const app = Vue.createApp(EducationDash);
app.mount('#_education-dash');
