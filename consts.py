"""
Global variables to be set by user
"""

window_width = 1200
window_height = 800
map_width = 1187
map_height = 655
zoom = 16
map_title = ''

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
TILES_OUTPUT_FOLDER = 'tiles'
MAPS_OUTPUT_FOLDER = 'maps'
SCREENSHOT_POSITION_REGEX = r'\w+_(\d+)_(\d+)'

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