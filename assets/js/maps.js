import * as settings from './conf';


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
