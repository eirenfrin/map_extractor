import consts as c
from boundaries_capturer import BoundariesCapturer as BC

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from driver_manager import DriverManager

newboundaries = BC()
newboundaries.getPoints()

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