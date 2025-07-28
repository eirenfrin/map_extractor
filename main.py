import consts as c
from boundaries_capturer import BoundariesCapturer as BC
from driver_manager import DriverManager as DM
from tiles_creator import TilesCreator as TC

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By



newboundaries = BC()
newboundaries.getPoints()
newboundaries.getLonLatFromURL()
print(newboundaries.map_coords)
tilesCreator = TC(newboundaries.map_coords)
for i, coord in enumerate(tilesCreator.map_coords):
    if i%2 == 1:
        continue
    if i == len(tilesCreator.map_coords)-1:
        break
    print(tilesCreator.getPixelDistanceFromLatLongCoords(coord, tilesCreator.map_coords[i+1]))


# new_driver = DM()
# new_driver.launchChromeWithSelenium(no_overlays=False)
# inner_width = new_driver.driver.execute_script("return window.innerWidth")
# inner_height = new_driver.driver.execute_script("return window.innerHeight")
# print(inner_height)
# print(inner_width)
# new_driver.closeDriver()


# output_folder = "tiles"
# os.makedirs(output_folder, exist_ok=True)

# options = Options()
# options.headless = True
# driver = webdriver.Chrome(options=options)
# driver.set_window_size(1200, 800)  #viewport size
# driver.get(c.URL.format(zoom=c.ZOOM, x=c.X_START, y=c.Y_START))

# driver.execute_script("""
#     document.querySelectorAll('header, .fm-type-zoom-control, div.fm-toolbar, div.leaflet-control-scale-line, div.fade').forEach(e => e.style.display = 'none');
# """)

# map_element = driver.find_element(By.CLASS_NAME, 'leaflet-container, leaflet-touch, leaflet-retina, leaflet-fade-anim, leaflet-grab, leaflet-touch-drag, leaflet-touch-zoom')
# dims = map_element.rect
# center_x = dims['width'] // 2
# center_y = dims['height'] // 2
# print(dims, center_x, center_y)

# urls = []

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
#     urls.append(driver.current_url)

#     full_path = os.path.join(output_folder, f'map_capture{i}.png')
#     driver.save_screenshot(full_path)

# driver.quit()
# print(urls)
# dims = map_element.rect
# center_x = dims['width'] // 2
# center_y = dims['height'] // 2
# print(dims)
# driver.quit()


