import consts as c

from PIL import Image
import os
import re

class ScreenshotStitcher:
    """
    Connects all screenshots into a full map. Uses indices in each capture title for locating them.

     Attributes:
        map_folder (str): Holds the title of the map
        input_path (str): Holds a full path where all partial captures of the map are located
        filenames_sorted (list): Holds all captures' titles sorted by their position starting from top left capture
    """
    
    def __init__(self, map_folder):
        self.map_folder = map_folder
        self.input_path = os.path.join(c.TILES_OUTPUT_FOLDER, map_folder)
        self.filenames_sorted = None

    def stitch_screenshots(self):
        map_params = self.get_map_size()
        map_width_pixel = map_params['width_first'] + map_params['width_next']*map_params['shifts']
        map_height_pixel = map_params['height']*map_params['bands']
        full_map = Image.new('RGB', (map_width_pixel, map_height_pixel))

        vertical_offshift = 0
        horizontal_offshift = 0
        num_captures_in_band = map_params['shifts']+1
        for capture_index, capture_filename in enumerate(self.filenames_sorted):
            capture_index = capture_index % num_captures_in_band

            capture = Image.open(os.path.join(self.input_path, capture_filename))
            full_map.paste(capture, (horizontal_offshift, vertical_offshift))

            if capture_index == 0:
                horizontal_offshift += map_params['width_first']

            elif capture_index == map_params['shifts']:
                vertical_offshift += map_params['height']
                horizontal_offshift = 0

            else: 
                horizontal_offshift += map_params['width_next']
        
        full_map.save(os.path.join(c.MAPS_OUTPUT_FOLDER, f'{self.map_folder}.png'))
   

    def get_map_size(self):
        filenames = [capture for capture in os.listdir(self.input_path) if os.path.isfile(os.path.join(self.input_path, capture))]
        self.filenames_sorted = sorted(filenames, key=lambda img: tuple(map(int, re.match(c.SCREENSHOT_POSITION_REGEX, img).groups())))

        bands, shifts = tuple(map(int, re.match(c.SCREENSHOT_POSITION_REGEX, self.filenames_sorted[-1]).groups()))

        width_first = self.get_image_size(self.filenames_sorted[0])['width']
        width_next, height = self.get_image_size(self.filenames_sorted[1]).values()

        return {
            'shifts': shifts,
            'bands': bands+1,
            'width_first': width_first,
            'width_next': width_next,
            'height': height
        }
    
    def get_image_size(self, filename):
        img = Image.open(os.path.join(self.input_path, filename))
        return {'width': int(img.width), 'height': int(img.height)}
        