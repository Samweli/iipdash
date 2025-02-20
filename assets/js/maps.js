import * as settings from './conf';

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
                'minzoom': 1,
                'maxzoom': 19
            }
        ]
    },
    center: settings.MAP_DEFAULT_CENTER,
    zoom: settings.MAP_DEFAULT_ZOOM
}


export const areasEducationTilesURL = settings.API_ROOT + 'administrative/areas-education/tiles/{z}/{x}/{y}.mvt/?level=2'


export const sources = {
    'areas-education': {
        type: 'vector',
        tiles: [areasEducationTilesURL],
        minzoom: 1,
        maxzoom: 19
    }
}


const areasEducationLayer = {
    id: 'areas-education',
    source: 'areas-education',
    'source-layer': 'areas-education',
    type: 'fill',
    paint: {
        "fill-opacity": 0.7,
        "fill-outline-color": "#007fff",
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
                30000, '#007fff'
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


export const layers = {
    'areas-education': areasEducationLayer,
}
