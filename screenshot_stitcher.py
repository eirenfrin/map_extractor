import consts as c

from PIL import Image
import os
import re

class ScreenshotStitcher:
    def __init__(self, map_folder):
        self.map_folder = map_folder

    def stitchScreenshots(self):
        map_params = self.getMapSize()
        map_width_pixel = map_params['width_first'] + map_params['width_next']*map_params['shifts']
        map_height_pixel = map_params['height']*(map_params['bands']+1)
        print(map_height_pixel)
        print(map_width_pixel)
        map = Image.new('RGB', (map_width_pixel, map_height_pixel))

        vertical_offshift = 0
        horizontal_offshift = 0
        for capture_index, capture_filename in enumerate(self.filenames_sorted):
            print(capture_filename)

            capture = Image.open(os.path.join(self.path, capture_filename))
            map.paste(capture, (horizontal_offshift, vertical_offshift))

            if capture_index == 0:
                horizontal_offshift += map_params['width_first']

            elif (capture_index+1) % (map_params['shifts']+1) == 0:
                vertical_offshift += map_params['height']
                horizontal_offshift = 0

            else: 
                horizontal_offshift += map_params['width_next']
        
        map.save(os.path.join(self.path, 'MAP.png'))
   

    def getMapSize(self):
        map_params = {
            'shifts': 0,
            'bands': 0,
            'width_first': 0,
            'width_next': 0,
            'height': 0
        }
        self.path = os.path.join(c.MAPS_OUTPUT_FOLDER, self.map_folder)
        filenames = [capture for capture in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, capture))]

        pattern = re.compile(r"capture_(\d+)_(\d+)\.\w+")
        self.filenames_sorted = sorted(filenames, key=lambda f: tuple(map(int, pattern.match(f).groups())))

        map_params['bands'], map_params['shifts'] = tuple(map(int, re.match(c.SCREENSHOT_POSITION_REGEX, self.filenames_sorted[-1]).groups()))

        for i, f in enumerate(self.filenames_sorted[:2]):
            img = Image.open(os.path.join(self.path, f))
            if i == 0:
                map_params['width_first'] = img.width
            else:
                map_params['width_next'] = img.width
                map_params['height'] = img.height

        return map_params