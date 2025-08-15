import consts as c
from boundaries_capturer import BoundariesCapturer as BC
from driver_manager import DriverManager as DM
from tiles_creator import TilesCreator as TC
from screenshot_maker import ScreenshotMaker as SM
from settings import Settings as S

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from decimal import Decimal


settings = S('with rounding', 1200, 800, 16)
settings.setWindowSizeZoom()
settings.setMapSize()
settings.setStorageFolders()

# newboundaries = BC()
# newboundaries.getPoints()
# newboundaries.storePoints()
tilesCreator = TC([])
tilesCreator.readMapCoords('no_rounding')
tilesCreator.convertToDecimal()
tilesCreator.getContainerRectangle()
tilesCreator.computeBandsShiftsNumber()
screenshotMaker = SM(tilesCreator.area)
screenshotMaker.moveAcrossBands()

