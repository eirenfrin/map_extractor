import consts as c
from driver_manager import DriverManager as DM

import os
import json
from datetime import datetime
from decimal import Decimal

class Settings:
    def __init__(self, map_title='', window_width=1200, window_height=800, zoom=16):
        self.map_title = '_'.join(map_title.split(' '))
        self.window_height = window_height
        self.window_width = window_width
        self.zoom = zoom

    def setWindowSizeZoom(self):
        c.WINDOW_HEIGHT = self.window_height
        c.WINDOW_WIDTH = self.window_width
        c.ZOOM = self.zoom

    def setMapSize(self):
        new_driver = DM()
        new_driver.launchChromeWithSelenium(no_overlays=False)
        map_element = new_driver.getMapElement()
        dims = map_element.rect
        # size = new_driver.driver.execute_script("""
        #     let map = document.getElementsByClassName('leaflet-container leaflet-touch leaflet-retina leaflet-fade-anim leaflet-grab leaflet-touch-drag leaflet-touch-zoom')[0]
        #     let rect = map.getBoundingClientRect();
        #     return {width: rect.width, height: rect.height};
        # """)

        # c.MAP_WIDTH = Decimal(str(size['width']))
        # c.MAP_HEIGHT = Decimal(str(size['height']))
        c.MAP_HEIGHT = dims['height']
        c.MAP_WIDTH = dims['width']

        new_driver.closeDriver()

    def setStorageFolders(self):
        os.makedirs(c.MAPS_OUTPUT_FOLDER, exist_ok=True)
        os.makedirs(c.BOUNDARIES_OUTPUT_FOLDER, exist_ok=True)

        if not self.map_title:
            current_time = datetime.now()
            self.map_title = current_time.strftime("%d_%m_%Y__%H_%M")

        c.MAP_TITLE = self.map_title

        tiles_storage_path = os.path.join(c.MAPS_OUTPUT_FOLDER, self.map_title)
        os.makedirs(tiles_storage_path, exist_ok=True)

        # open(os.path.join(c.BOUNDARIES_OUTPUT_FOLDER, self.map_title), "w").close()
        with open(os.path.join(c.BOUNDARIES_OUTPUT_FOLDER, f"{self.map_title}.json"), "w") as boundaries_storage:
            json.dump([], boundaries_storage)

