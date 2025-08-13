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


settings = S('test map', 1200, 800, 16)
settings.setWindowSizeZoom()
settings.setMapSize()
settings.setStorageFolders()

newboundaries = BC()
newboundaries.getPoints()
tilesCreator = TC(newboundaries.map_coords)
tilesCreator.getContainerRectangle()
tilesCreator.computeBandsShiftsNumber()
screenshotMaker = SM(tilesCreator.area)
screenshotMaker.moveAcrossBands()


