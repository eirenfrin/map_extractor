"""
Constants to be set by user
"""

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
MAP_WIDTH = 1187
MAP_HEIGHT = 655
ZOOM = 16
MAP_TITLE = ''

"""
Regular constants
"""

X_START = 17 # longitude
Y_START = 48 # latitude
TILE_SIZE = 256
XYZ_URL_REGEX = r'\d+(?:\.\d+)?'


URL = 'https://www.freemap.sk/#map={zoom}/{y}/{x}&layers=X'
MAP_CONTAINER_CLASSES = 'leaflet-container, leaflet-touch, leaflet-retina, leaflet-fade-anim, leaflet-grab, leaflet-touch-drag, leaflet-touch-zoom'
OVERLAY_ELEMENTS_CLASSES = 'header, .fm-type-zoom-control, div.fm-toolbar, div.leaflet-control-scale-line, div.fade'

BOUNDARIES_OUTPUT_FOLDER = 'boundaries'
MAPS_OUTPUT_FOLDER = 'maps'

BOUNDARIES_SCRIPT = """
    try{
    window.boundaryPoint = null;
    window.selectionMode = true;
    window.newPointToStore = false;
    let map = document.getElementsByClassName('leaflet-container leaflet-touch leaflet-retina leaflet-fade-anim leaflet-grab leaflet-touch-drag leaflet-touch-zoom')[0]

    let lastMousePos = null;
                        
    map.addEventListener('mousemove', function (e) {
        const rect = map.getBoundingClientRect();
        lastMousePos = {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };
    });

    window.addEventListener('keydown', function(event) {
        if (event.key === 'b') {
            window.boundaryPoint = lastMousePos.x + '_' + lastMousePos.y;
            window.newPointToStore = true
        }
        if (event.key === 'Enter') {
            window.selectionMode = false;
        }
    });
    }
    catch (e) { }
"""