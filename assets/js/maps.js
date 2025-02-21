import * as settings from './conf';



export const defaultMinZoom = 1;
export const defaultMaxZoom = 19;

const colorPrimary = "#007fff";

// The default basemap style
export const basemap = {
    style: {
        'version': 8,
        'sources': {
            'basemap': {
                'type': 'raster',
                'tiles': [settings.BASEMAP_URL],
                'tileSize': 256,
                'attribution': settings.BASEMAP_ATTRIBUTION
            }
        },
        'layers': [
            {
                'id': 'basemap',
                'type': 'raster',
                'source': 'basemap',
                'minzoom': defaultMinZoom,
                'maxzoom': defaultMaxZoom
            }
        ]
    },
    center: settings.MAP_DEFAULT_CENTER,
    zoom: settings.MAP_DEFAULT_ZOOM
}


export const countriesTilesURL = settings.API_ROOT + 'administrative/areas/tiles/{z}/{x}/{y}.mvt/?level=1'
export const educationInstitutionsTilesUrl = settings.API_ROOT + 'education/institutions/tiles/{z}/{x}/{y}.mvt/'
export const fiberNodesTilesUrl = settings.API_ROOT + 'infrastructure/fiber-nodes/tiles/{z}/{x}/{y}.mvt/'
export const areasEducationTilesURL = settings.API_ROOT + 'administrative/areas-education/tiles/{z}/{x}/{y}.mvt/?level=2'


export const sources = {
    'countries': {
        type: 'vector',
        tiles: [countriesTilesURL],
        minzoom: defaultMinZoom,
        maxzoom: defaultMaxZoom
    },
    'areas-education': {
        type: 'vector',
        tiles: [areasEducationTilesURL],
        minzoom: defaultMinZoom,
        maxzoom: defaultMaxZoom
    },
    'education-institutions': {
        type: 'vector',
        tiles: [educationInstitutionsTilesUrl],
        minzoom: defaultMinZoom,
        maxzoom: defaultMaxZoom
    },
    'fiber-nodes': {
        type: 'vector',
        tiles: [fiberNodesTilesUrl],
        minzoom: defaultMinZoom,
        maxzoom: defaultMaxZoom
    }
}


const countriesLayer = {
    id: 'countries',
    source: 'countries',
    'source-layer': 'administrative-areas',
    type: 'line',
    paint: {
        'line-width': 2.7,
        'line-color': colorPrimary,
    }
};


const areasEducationLayer = {
    id: 'areas-education',
    source: 'areas-education',
    'source-layer': 'areas-education',
    type: 'fill',
    paint: {
        "fill-outline-color": colorPrimary,
        'fill-color': [
            'case',
            ['==', ['get', 'institutions_fiber_distance_median'], null],
            'rgba(0, 0, 0, 0)',
            [
                'interpolate',  // interpolation expression
                ['linear'],  // interpolation type
                ['get', 'institutions_fiber_distance_median'],  // value to be used for interpolation
                // color stops,
                0, '#ffffff',
                1000, '#dae1ff',
                30000, colorPrimary
            ]
        ],
        'fill-opacity': [ // Zoom-dependent opacity
            'interpolate',
            ['linear'],
            ['zoom'],
            0, 1.0, // Opacity at zoom level 0
            5, 0.7, // Opacity at zoom level 5
            10, 0.3  // Opacity at zoom level 10
        ],
    }
};


const educationInstitutionsLayer = {
    id: 'education-institutions',
    source: 'education-institutions',
    'source-layer': 'education-institutions',
    type: 'circle',
    paint: {
        "circle-blur": 0,
        "circle-color": colorPrimary,
        "circle-opacity": 0.9,
        "circle-stroke-opacity": 0,
        "circle-stroke-width": 0,
        'circle-radius': [ // Zoom-dependent circle radius
            'interpolate',
            ['linear'],
            ['zoom'],
            0, 0.5, // zoom level 0
            5, 2.0, // zoom level 5
            10, 3.0,  // zoom level 10
            14, 5.0  // zoom level 14
        ],
    }
}

const fiberNodesLayer = {
    id: 'fiber-nodes',
    source: 'fiber-nodes',
    'source-layer': 'fiber-nodes',
    type: 'circle',
    paint: {
        'circle-blur': 0,
        'circle-color': '#ffffff',
        'circle-opacity': 0.5,
        'circle-stroke-color': '#AEA79F',
        'circle-stroke-opacity': 0.9,
        'circle-stroke-width': 2,
        'circle-radius': [ // Zoom-dependent circle radius
            'interpolate',
            ['linear'],
            ['zoom'],
            0, 1.0, // zoom level 0
            5, 5.0, // zoom level 5
            10, 10.0,  // zoom level 10
            14, 14.0  // zoom level 14
        ],
    }
}


export const layers = {
    'countries': countriesLayer,
    'areas-education': areasEducationLayer,
    'education-institutions': educationInstitutionsLayer,
    'fiber-nodes': fiberNodesLayer
}
