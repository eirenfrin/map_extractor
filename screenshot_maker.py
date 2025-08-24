import consts as c
from driver_manager import DriverManager as DM

from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from PIL import Image
import io

class ScreenshotMaker:
    """
    At each distinct latutide (band) opens a new Chrome window and moves horizontally for the specified number of shifts.
    While moving makes screenshots of the views.

     Attributes:
        area (list): Contains lists with a two-element tuple and an integer, [(lat, long), number]
        band_number (int): Holds a currently processed band index
        tile_number (int): Holds a currently processed tile index
    """

    def __init__(self, area):
        self.area = area 
        self.band_number = 0
        self.tile_number = 0

    def move_across_bands(self):
        for band_number, band in enumerate(self.area):
            self.band_number = band_number

            (lat, long), num_shifts = band
            self.shift_horizontally(long, lat, num_shifts)
        
    def shift_horizontally(self, long, lat, num_shifts):
        new_driver = DM()
        new_driver.launch_chrome_with_selenium(x_start=long, y_start=lat)
        map_element = new_driver.get_map_element()
        center_x = c.map_width // 2
        remainder = c.map_width % 2

        for shift in range(num_shifts+1):
            time.sleep(3)
            self.tile_number = shift
            self.make_screenshot(new_driver, shift)

            self.shift_right(new_driver.get_driver(), map_element, center_x)
            self.shift_right(new_driver.get_driver(), map_element, center_x)
            if remainder:
                self.shift_right(new_driver.get_driver(), map_element, remainder)
        
        new_driver.close_driver()

    def make_screenshot(self, driver, crop):
        full_path = os.path.join(c.TILES_OUTPUT_FOLDER, c.map_title, f'capture_{self.band_number}_{self.tile_number}.png')
        capture = driver.driver.get_screenshot_as_png()
        img = Image.open(io.BytesIO(capture))

        if crop:
            img = img.crop((2, 0, img.width, img.height))

        img.save(full_path)

    def shift_right(self, driver, map_element, step):
        ActionChains(driver).move_to_element_with_offset(map_element, 0, 0)\
        .click_and_hold()\
        .move_by_offset(-step, 0)\
        .pause(0.5).release().perform()
        time.sleep(1)

