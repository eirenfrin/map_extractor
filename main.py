from boundaries_capturer import BoundariesCapturer as BC
from tiles_creator import TilesCreator as TC
from screenshot_maker import ScreenshotMaker as SM
from settings import Settings as S
from screenshot_stitcher import ScreenshotStitcher as SS

# >>>>>>>>> creates folders for outputs and sets global variables <<<<<<<<<

settings = S('map', 1200, 800, 15)
settings.set_window_size_zoom()
settings.set_map_size()
settings.set_storage_folders()

# >>>>>>>>> collects and stores coordinates to be included in the map <<<<<<<<<

newboundaries = BC()
newboundaries.get_points()
newboundaries.store_points()

# >>>>>>>>> computes boundaries of the map and divides it into tiles <<<<<<<<<

# sonarignore: python:S125
# tilesCreator = TC([])
tilesCreator = TC(newboundaries.map_coords)
# tilesCreator.readMapCoords('last_test')
tilesCreator.convert_to_decimal()
tilesCreator.get_container_rectangle()
tilesCreator.compute_bands_shifts_number()

# >>>>>>>>> makes screenshots according to computed tiles <<<<<<<<<

screenshotMaker = SM(tilesCreator.area)
screenshotMaker.move_across_bands()

# >>>>>>>>> stitches individual screenshots into a full map <<<<<<<<<

ss = SS('map')
ss.stitch_screenshots()