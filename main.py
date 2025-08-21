import consts as c
from boundaries_capturer import BoundariesCapturer as BC
from driver_manager import DriverManager as DM
from tiles_creator import TilesCreator as TC
from screenshot_maker import ScreenshotMaker as SM
from settings import Settings as S
from screenshot_stitcher import ScreenshotStitcher as SS

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from decimal import Decimal


# settings = S('map', 1200, 800, 15)
# settings.setWindowSizeZoom()
# settings.setMapSize()
# settings.setStorageFolders()
# print(c.ZOOM)
# newboundaries = BC()
# newboundaries.getPoints()

# newboundaries.storePoints()
# # tilesCreator = TC([])
# tilesCreator = TC(newboundaries.map_coords)
# # tilesCreator.readMapCoords('last_test')
# tilesCreator.convertToDecimal()
# tilesCreator.getContainerRectangle()
# tilesCreator.computeBandsShiftsNumber()
# screenshotMaker = SM(tilesCreator.area)
# screenshotMaker.moveAcrossBands()

ss = SS('full_map')
print(ss.getMapSize())
ss.stitchScreenshots()