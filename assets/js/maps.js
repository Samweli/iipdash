import axios from 'axios';

import * as settings from './conf';

export const defaultMinZoom = 1;
export const defaultMaxZoom = 19;

const colorPrimary = settings.COLOR_PRIMARY;
const API_ROOT = settings.API_ROOT;

// The default basemap style
export const basemap = {
    style: {
        version: 8,
        sources: {
            basemap: {
                type: 'raster',
                tiles: [settings.BASEMAP_URL],
                tileSize: 256,
                attribution: settings.BASEMAP_ATTRIBUTION,
            },
        },
        layers: [
            {
                id: 'basemap',
                type: 'raster',
                source: 'basemap',
                minzoom: defaultMinZoom,
                maxzoom: defaultMaxZoom,
            },
        ],
    },
    center: settings.MAP_DEFAULT_CENTER,
    zoom: settings.MAP_DEFAULT_ZOOM,
};

export const countriesTilesURL = API_ROOT + 'administrative/areas/tiles/{z}/{x}/{y}.mvt/?level=2';
export const regionsTilesURL = API_ROOT + 'administrative/areas/tiles/{z}/{x}/{y}.mvt/?level=3';
export const populationDensityHDTilesURL = API_ROOT + 'demographics/population-density-hd/tiles/{z}/{x}/{y}.mvt/';
export const educationInstitutionsTilesUrl = API_ROOT + 'education/institutions/tiles/{z}/{x}/{y}.mvt/';
export const healthFacilitiesTilesUrl = API_ROOT + 'health/health-facilities/tiles/{z}/{x}/{y}.mvt/';
export const fiberOpticsTilesUrl = API_ROOT + 'infrastructure/fiber-optics/tiles/{z}/{x}/{y}.mvt/';
export const fiberNodesTilesUrl = API_ROOT + 'infrastructure/fiber-nodes/tiles/{z}/{x}/{y}.mvt/';
export const cellTowersTilesUrl = API_ROOT + 'infrastructure/cell-towers/tiles/{z}/{x}/{y}.mvt/';
export const areasEducationTilesURL = API_ROOT + 'administrative/areas-education/tiles/{z}/{x}/{y}.mvt/?level=3';
export const areasMobileCoverageTilesURL =
    API_ROOT + 'administrative/areas-mobile-coverage/tiles/{z}/{x}/{y}.mvt/?level=3';

export const getMobileCoverageTMSURLs = async (lookup) => {
    try {
        const mobileCoverages = await axios.get(`${API_ROOT}infrastructure/mobile-coverage/`, {
            params: { ...lookup, tiff_empty: false },
        });

        return mobileCoverages.data.results.map((coverage) => {
            return coverage.tms_url;
        });
    } catch (e) {
        console.log(e); // eslint-disable-line no-console
        return [];
    }
};

export const sources = {
    countries: {
        type: 'vector',
        tiles: [countriesTilesURL],
        minzoom: defaultMinZoom,
        maxzoom: defaultMaxZoom,
    },
    regions: {
        type: 'vector',
        tiles: [regionsTilesURL],
        minzoom: defaultMinZoom,
        maxzoom: defaultMaxZoom,
    },
    'fiber-optics': {
        type: 'vector',
        tiles: [fiberOpticsTilesUrl],
        minzoom: defaultMinZoom,
        maxzoom: defaultMaxZoom,
    },
    'population-density-hd': {
        type: 'vector',
        tiles: [populationDensityHDTilesURL],
        minzoom: defaultMinZoom,
        maxzoom: defaultMaxZoom,
    },
    'areas-education': {
        type: 'vector',
        tiles: [areasEducationTilesURL],
        minzoom: defaultMinZoom,
        maxzoom: defaultMaxZoom,
    },
    'areas-mobile-coverage': {
        type: 'vector',
        tiles: [areasMobileCoverageTilesURL],
        minzoom: defaultMinZoom,
        maxzoom: defaultMaxZoom,
    },
    'education-institutions': {
        type: 'vector',
        tiles: [educationInstitutionsTilesUrl],
        minzoom: defaultMinZoom,
        maxzoom: defaultMaxZoom,
    },
    'health-facilities': {
        type: 'vector',
        tiles: [healthFacilitiesTilesUrl],
        minzoom: defaultMinZoom,
        maxzoom: defaultMaxZoom,
    },
    'fiber-nodes': {
        type: 'vector',
        tiles: [fiberNodesTilesUrl],
        minzoom: defaultMinZoom,
        maxzoom: defaultMaxZoom,
    },
    'cell-towers': {
        type: 'vector',
        tiles: [cellTowersTilesUrl],
        minzoom: defaultMinZoom,
        maxzoom: defaultMaxZoom,
    },
    'mobile-coverage-3g': {
        type: 'raster',
        tiles: await getMobileCoverageTMSURLs({
            network_generation_code: '3g',
            administrative_area_level: settings.ADMINISTRATIVE_AREA_ALL_COUNTRIES_LEVEL,
        }),
        tileSize: 256,
        scheme: 'tms',
    },
    'mobile-coverage-4g': {
        type: 'raster',
        tiles: await getMobileCoverageTMSURLs({
            network_generation_code: '4g',
            administrative_area_level: settings.ADMINISTRATIVE_AREA_ALL_COUNTRIES_LEVEL,
        }),
        tileSize: 256,
        scheme: 'tms',
    },
};

const countriesLayer = {
    id: 'countries',
    source: 'countries',
    'source-layer': 'administrative-areas',
    type: 'line',
    paint: {
        'line-width': 2.7,
        'line-color': colorPrimary,
    },
};

const regionsLayer = {
    id: 'regions',
    source: 'regions',
    'source-layer': 'administrative-areas',
    type: 'line',
    paint: {
        'line-width': 2.0,
        'line-color': colorPrimary,
    },
};

const fiberOpticsLayer = {
    id: 'fiber-optics',
    source: 'fiber-optics',
    'source-layer': 'fiber-optics',
    type: 'line',
    paint: {
        'line-width': 2.0,
        'line-color': '#64687A',
    },
};

const populationDensityHDLayer = {
    id: 'population-density-hd',
    source: 'population-density-hd',
    'source-layer': 'population-density-hd',
    type: 'circle',
    paint: {
        'circle-blur': 0,
        'circle-color': [
            'case',
            ['==', ['get', 'population_density'], null],
            'rgba(0, 0, 0, 0)',
            [
                'interpolate', // interpolation expression
                ['linear'], // interpolation type
                ['get', 'population_density'], // value to be used for interpolation
                // color stops,
                0,
                '#ffffff',
                1,
                '#dae1ff',
                30,
                colorPrimary,
            ],
        ],
        'circle-stroke-opacity': 0,
        'circle-stroke-width': 0,
        'circle-opacity': 0.9,
        'circle-radius': [
            // Zoom-dependent circle radius
            'interpolate',
            ['linear'],
            ['zoom'],
            0,
            0.1, // zoom level 0
            11,
            1.0, // zoom level 10
            14,
            3.0, // zoom level 14
        ],
    },
};

const areasEducationLayer = {
    id: 'areas-education',
    source: 'areas-education',
    'source-layer': 'areas-education',
    type: 'fill',
    paint: {
        'fill-outline-color': colorPrimary,
        'fill-color': [
            'case',
            ['==', ['get', 'institutions_fiber_distance_median'], null],
            'rgba(0, 0, 0, 0)',
            [
                'interpolate', // interpolation expression
                ['linear'], // interpolation type
                ['get', 'institutions_fiber_distance_median'], // value to be used for interpolation
                // color stops,
                0,
                '#ffffff',
                1000,
                '#dae1ff',
                30000,
                colorPrimary,
            ],
        ],
        'fill-opacity': [
            // Zoom-dependent opacity
            'interpolate',
            ['linear'],
            ['zoom'],
            0,
            1.0, // Opacity at zoom level 0
            5,
            0.7, // Opacity at zoom level 5
            10,
            0.3, // Opacity at zoom level 10
        ],
    },
};

const areasMobileCoverage3GLayer = {
    id: 'areas-mobile-coverage-3g',
    source: 'areas-mobile-coverage',
    'source-layer': 'areas-mobile-coverage',
    type: 'fill',
    paint: {
        'fill-outline-color': colorPrimary,
        'fill-color': [
            'case',
            ['==', ['get', 'coverage_3g'], null],
            'rgba(0, 0, 0, 0)',
            [
                'interpolate', // interpolation expression
                ['linear'], // interpolation type
                ['get', 'coverage_3g'], // value to be used for interpolation
                // color stops,
                0,
                '#ffffff',
                1,
                '#dae1ff',
                70,
                colorPrimary,
            ],
        ],
        'fill-opacity': [
            // Zoom-dependent opacity
            'interpolate',
            ['linear'],
            ['zoom'],
            0,
            1.0, // Opacity at zoom level 0
            5,
            0.7, // Opacity at zoom level 5
            10,
            0.3, // Opacity at zoom level 10
        ],
    },
};

const areasMobileCoverage4GLayer = {
    id: 'areas-mobile-coverage-4g',
    source: 'areas-mobile-coverage',
    'source-layer': 'areas-mobile-coverage',
    type: 'fill',
    paint: {
        'fill-outline-color': colorPrimary,
        'fill-color': [
            'case',
            ['==', ['get', 'coverage_4g'], null],
            'rgba(0, 0, 0, 0)',
            [
                'interpolate', // interpolation expression
                ['linear'], // interpolation type
                ['get', 'coverage_4g'], // value to be used for interpolation
                // color stops,
                0,
                '#ffffff',
                1,
                '#dae1ff',
                70,
                colorPrimary,
            ],
        ],
        'fill-opacity': [
            // Zoom-dependent opacity
            'interpolate',
            ['linear'],
            ['zoom'],
            0,
            1.0, // Opacity at zoom level 0
            5,
            0.7, // Opacity at zoom level 5
            10,
            0.3, // Opacity at zoom level 10
        ],
    },
};

const educationInstitutionsLayer = {
    id: 'education-institutions',
    source: 'education-institutions',
    'source-layer': 'education-institutions',
    type: 'circle',
    paint: {
        'circle-blur': 0,
        'circle-color': colorPrimary,
        'circle-opacity': 0.9,
        'circle-stroke-opacity': 0,
        'circle-stroke-width': 0,
        'circle-radius': [
            // Zoom-dependent circle radius
            'interpolate',
            ['linear'],
            ['zoom'],
            0,
            0.5, // zoom level 0
            5,
            2.0, // zoom level 5
            10,
            3.0, // zoom level 10
            14,
            5.0, // zoom level 14
        ],
    },
};

const healthFacilitiesLayer = {
    id: 'health-facilities',
    source: 'health-facilities',
    'source-layer': 'health-facilities',
    type: 'circle',
    paint: {
        'circle-blur': 0,
        'circle-color': '#ffffff',
        'circle-opacity': 0.8,
        'circle-stroke-color': '#007FFF',
        'circle-stroke-opacity': 0.9,
        'circle-stroke-width': 2,
        'circle-radius': [
            // Zoom-dependent circle radius
            'interpolate',
            ['linear'],
            ['zoom'],
            0,
            1.0, // zoom level 0
            5,
            5.0, // zoom level 5
            10,
            10.0, // zoom level 10
            14,
            14.0, // zoom level 14
        ],
    },
};

const fiberNodesLayer = {
    id: 'fiber-nodes',
    source: 'fiber-nodes',
    'source-layer': 'fiber-nodes',
    type: 'circle',
    paint: {
        'circle-blur': 0,
        'circle-color': '#ffffff',
        'circle-opacity': 0.7,
        'circle-stroke-color': '#AEA79F',
        'circle-stroke-opacity': 0.9,
        'circle-stroke-width': 2,
        'circle-radius': [
            // Zoom-dependent circle radius
            'interpolate',
            ['linear'],
            ['zoom'],
            0,
            1.0, // zoom level 0
            5,
            5.0, // zoom level 5
            10,
            10.0, // zoom level 10
            14,
            14.0, // zoom level 14
        ],
    },
};

const cellTowersLayer = {
    id: 'cell-towers',
    source: 'cell-towers',
    'source-layer': 'cell-towers',
    type: 'circle',
    paint: {
        'circle-blur': 0,
        // Fill color
        'circle-color': '#82A5FF',
        // Fill opacity
        'circle-opacity': 0.5,
        // Border color
        'circle-stroke-color': '#007FFF',
        'circle-stroke-opacity': 1,
        'circle-stroke-width': 2,
        // Radius based on "range" property
        'circle-radius': [
            'interpolate',
            ['linear'],
            ['get', 'range'], // value to be used for interpolation
            0,
            1,
            100,
            2,
            500,
            3,
            2000,
            6,
            5000,
            8,
            10000,
            10,
            20000,
            12,
            40000,
            14,
            80000,
            15, // Flattens the growth beyond 80,000 meters
        ],
    },
};

const mobileCoverage3GLayer = {
    id: 'mobile-coverage-3g',
    type: 'raster',
    source: 'mobile-coverage-3g',
    minzoom: defaultMinZoom,
    maxzoom: defaultMaxZoom,
};

const mobileCoverage4GLayer = {
    id: 'mobile-coverage-4g',
    type: 'raster',
    source: 'mobile-coverage-4g',
    minzoom: defaultMinZoom,
    maxzoom: defaultMaxZoom,
};

export const layers = {
    countries: countriesLayer,
    regions: regionsLayer,
    'fiber-optics': fiberOpticsLayer,
    'population-density-hd': populationDensityHDLayer,
    'areas-education': areasEducationLayer,
    'areas-mobile-coverage-3g': areasMobileCoverage3GLayer,
    'areas-mobile-coverage-4g': areasMobileCoverage4GLayer,
    'education-institutions': educationInstitutionsLayer,
    'health-facilities': healthFacilitiesLayer,
    'fiber-nodes': fiberNodesLayer,
    'cell-towers': cellTowersLayer,
    'mobile-coverage-3g': mobileCoverage3GLayer,
    'mobile-coverage-4g': mobileCoverage4GLayer,
};
