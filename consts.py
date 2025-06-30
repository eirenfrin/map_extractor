ZOOM = 16
X_START = 48
Y_START = 17

URL = 'https://www.freemap.sk/#map={zoom}/{x}/{y}&layers=X'
MAP_CONTAINER_CLASSES = 'leaflet-container leaflet-touch leaflet-retina leaflet-fade-anim leaflet-grab leaflet-touch-drag leaflet-touch-zoom'
OVERLAY_ELEMENTS_CLASSES = 'header, .fm-type-zoom-control, div.fm-toolbar, div.leaflet-control-scale-line, div.fade'

BOUNDARIES_OUTPUT_FOLDER = 'boundaries'
MAPS_OUTPUT_FOLDER = 'maps'

BOUNDARIES_SCRIPT = """
    try{
    window.boundaryPoints = [];
    window.selectionMode = true;
    map = document.getElementsByClassName('leaflet-container leaflet-touch leaflet-retina leaflet-fade-anim leaflet-grab leaflet-touch-drag leaflet-touch-zoom')[0]

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
            window.boundaryPoints.push({ x: lastMousePos.x, y: lastMousePos.y });
        }
        if (event.key === 'Enter') {
            window.selectionMode = false;
            alert("Selection finished.");
        }
    });
    }
    catch (e) { }
"""