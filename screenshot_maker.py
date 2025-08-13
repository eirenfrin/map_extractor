import consts as c
from driver_manager import DriverManager as DM

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import os

class ScreenshotMaker:
    def __init__(self, area):
        self.area = area # array of arrays as [(), number]
        self.band_number = 0
        self.tile_number = 0

    def moveAcrossBands(self):
        for band_number, band in enumerate(self.area):
            self.band_number = band_number

            (lat, long), num_shifts = band
            print(num_shifts)
            self.shiftHorizontally(long, lat, num_shifts)
        
    def shiftHorizontally(self, long, lat, num_shifts):
        new_driver = DM()
        new_driver.launchChromeWithSelenium(x_start=long, y_start=lat, no_overlays=True)
        map_element = new_driver.getMapElement()
        center_x = c.MAP_WIDTH // 2
        remainder = c.MAP_WIDTH % 2

        for shift in range(num_shifts+1):
            time.sleep(1)
            self.tile_number = shift
            self.makeScreenshot(new_driver)

            self.shiftRight(new_driver.getDriver(), map_element, center_x)
            self.shiftRight(new_driver.getDriver(), map_element, center_x)
            if remainder:
                print('remainder ', remainder)
                self.shiftRight(new_driver.getDriver(), map_element, remainder)
        
        new_driver.closeDriver()

    def makeScreenshot(self, driver):
        full_path = os.path.join(c.MAPS_OUTPUT_FOLDER, c.MAP_TITLE, f'capture_{self.band_number}_{self.tile_number}.png')
        driver.driver.save_screenshot(full_path)

    def shiftRight(self, driver, map_element, step):
        ActionChains(driver).move_to_element_with_offset(map_element, 0, 0)\
        .click_and_hold()\
        .move_by_offset(-step, 0)\
        .pause(0.5).release().perform()
        time.sleep(1)