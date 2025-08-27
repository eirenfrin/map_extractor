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

    def get_params_from_json(self):
        json_path = os.path.join(c.BOUNDARIES_OUTPUT_FOLDER, f"{self.map_title}.json")

        if(os.path.isfile(json_path)):
            with open(json_path, "r") as boundaries_storage:
                json_all = json.load(boundaries_storage)
                self.window_height = json_all["params"]["viewport_height"]
                self.window_width = json_all["params"]["viewport_width"]
                self.zoom = json_all["params"]["zoom"]
        else:
            raise FileNotFoundError(f"File '{self.map_title}.json' does not exist.")
        
    def check_tiles_title_taken(self):
        tiles_storage_path = os.path.join(c.TILES_OUTPUT_FOLDER, self.map_title)
        if os.path.isdir(tiles_storage_path):
            raise FileExistsError(f"Folder '{c.TILES_OUTPUT_FOLDER}\\{self.map_title}' already exists.")
        
    def check_title_json_taken(self):
        json_path = os.path.join(c.BOUNDARIES_OUTPUT_FOLDER, f"{self.map_title}.json")
        if(os.path.isfile(json_path)):
            raise FileExistsError(f"File '{self.map_title}.json' already exists.")

    def check_title_png_taken(self):
        png_map_path = os.path.join(c.MAPS_OUTPUT_FOLDER, f"{self.map_title}.png")
        if(os.path.isfile(png_map_path)):
            raise FileExistsError(f"File '{self.map_title}.png' already exists.")

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

    def set_map_title(self):
        if not self.map_title:
            current_time = datetime.now()
            self.map_title = current_time.strftime("%d_%m_%Y__%H_%M")

        c.map_title = self.map_title

    def set_tiles_output_folder(self):
        os.makedirs(c.TILES_OUTPUT_FOLDER, exist_ok=True)

        tiles_storage_path = os.path.join(c.TILES_OUTPUT_FOLDER, self.map_title)
        if os.path.isdir(tiles_storage_path):
            raise FileExistsError(f"Folder '{c.TILES_OUTPUT_FOLDER}\\{self.map_title}' already exists.")
        else:
            os.makedirs(tiles_storage_path, exist_ok=True)

    def set_boundaries_output_folder(self):
        os.makedirs(c.BOUNDARIES_OUTPUT_FOLDER, exist_ok=True)

        json_data = {
            "params": {
                "viewport_width": self.window_width,
                "viewport_height": self.window_height,
                "zoom": self.zoom
            },
            "data": []
        }

        with open(os.path.join(c.BOUNDARIES_OUTPUT_FOLDER, f"{self.map_title}.json"), "w") as boundaries_storage:
            json.dump(json_data, boundaries_storage)

    def set_maps_output_folder(self):
        os.makedirs(c.MAPS_OUTPUT_FOLDER, exist_ok=True)

    def check_tiles_exist(self):
        tiles_storage_path = os.path.join(c.TILES_OUTPUT_FOLDER, self.map_title)
        if not os.path.isdir(tiles_storage_path):
            raise FileNotFoundError(f"Folder '{c.TILES_OUTPUT_FOLDER}\\{self.map_title}' does not exist.")


