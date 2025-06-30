import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from driver_manager import DriverManager

newdriver = DriverManager()
newdriver.launchCromeWithSelenium(no_overlays=False)

script = """

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
        console.log(boundaryPoints)
    }
    if (event.key === 'Enter') {
        window.selectionMode = false;
        alert("Selection finished.");
    }
});

}
catch (e) { }

            
"""


boundaries = newdriver.injectScript(script, 'boundaryPoints')
print(boundaries)
newdriver.closeDriver()


# making screenshots
# hide all the overlays

# driver.execute_script("""
#     document.querySelectorAll('header, .fm-type-zoom-control, div.fm-toolbar, div.leaflet-control-scale-line, div.fade').forEach(e => e.style.display = 'none');
# """)

# map_element = driver.find_element(By.CLASS_NAME, 'leaflet-container, leaflet-touch, leaflet-retina, leaflet-fade-anim, leaflet-grab, leaflet-touch-drag, leaflet-touch-zoom')
# dims = map_element.rect
# center_x = dims['width'] // 2
# center_y = dims['height'] // 2
# print(dims, center_x, center_y)

# for i in range(3):
#     # drag to left or -right
#     # starts at the center of viewport (element)
#     ActionChains(driver).move_to_element_with_offset(map_element, 0, 0)\
#         .click_and_hold()\
#         .move_by_offset(-center_x, 0)\
#         .pause(0.5).release().perform()
    
#     ActionChains(driver).move_to_element_with_offset(map_element, 0, 0)\
#         .click_and_hold()\
#         .move_by_offset(-center_x, 0)\
#         .pause(0.5).release().perform()
    
#     time.sleep(1)  # wait for the map to render

#     full_path = os.path.join(output_folder, f'map_capture{i}.png')
#     driver.save_screenshot(full_path)

# driver.quit()

# dims = map_element.rect
# center_x = dims['width'] // 2
# center_y = dims['height'] // 2
# print(dims)