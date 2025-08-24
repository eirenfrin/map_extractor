import consts as c
from driver_manager import DriverManager as DM

import os
import json
from datetime import datetime

class Settings:
    """
    Creates all the necessary output folders. Calibrates map web element dimentions to user-defined viewport size.

     Attributes:
        map_title (str): Holds the title of the map
        window_height (int): Holds user-defined viewport height for capture collection
        window_width (int): Holds user-defined viewport width for capture collection
        zoom (int): Holds user-defined map zoom for capture collection
    """

    def __init__(self, map_title='', window_width=1200, window_height=800, zoom=16):
        self.map_title = '_'.join(map_title.split(' '))
        self.window_height = window_height
        self.window_width = window_width
        self.zoom = zoom

    def set_window_size_zoom(self):
        c.window_height = self.window_height
        c.window_width = self.window_width
        c.zoom = self.zoom

    def set_map_size(self):
        new_driver = DM()
        new_driver.launch_chrome_with_selenium(no_overlays=False)
        map_element = new_driver.get_map_element()
        dims = map_element.rect
        
        c.map_height = dims['height']
        c.map_width = dims['width']

        new_driver.close_driver()

    def set_storage_folders(self):
        os.makedirs(c.TILES_OUTPUT_FOLDER, exist_ok=True)
        os.makedirs(c.BOUNDARIES_OUTPUT_FOLDER, exist_ok=True)
        os.makedirs(c.MAPS_OUTPUT_FOLDER, exist_ok=True)

        if not self.map_title:
            current_time = datetime.now()
            self.map_title = current_time.strftime("%d_%m_%Y__%H_%M")

        c.map_title = self.map_title

        tiles_storage_path = os.path.join(c.TILES_OUTPUT_FOLDER, self.map_title)
        os.makedirs(tiles_storage_path, exist_ok=True)

        with open(os.path.join(c.BOUNDARIES_OUTPUT_FOLDER, f"{self.map_title}.json"), "w") as boundaries_storage:
            json.dump([], boundaries_storage)

