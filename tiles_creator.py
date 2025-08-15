import consts as c

from decimal import Decimal, getcontext, ROUND_HALF_UP, ROUND_UP
import math
import os
import json

class TilesCreator:
    def __init__(self, map_coords):
        self.map_coords = map_coords # list of (lat, long) tuples str type
        self.area = []

    def convertToDecimal(self):
        self.map_coords = [(Decimal(lat), Decimal(long)) for lat, long in self.map_coords]
        print(self.map_coords)

    def readMapCoords(self, map_title=None):
        with open(os.path.join(c.BOUNDARIES_OUTPUT_FOLDER, f"{map_title if map_title else c.MAP_TITLE}.json"), "r") as boundaries_storage:
            map_coords_as_lists = json.load(boundaries_storage)
            self.map_coords = [tuple(coords) for coords in map_coords_as_lists]
            print(self.map_coords)

    def getMinMaxLongitudeCoord(self):
        _, long = zip(*self.map_coords)
        return (min(long), max(long))

    def getMinMaxLatitudeCoord(self):
        lat, _ = zip(*self.map_coords)
        return (min(lat), max(lat))
    
    def getContainerRectangle(self):
        min_max_latitude_coord = self.getMinMaxLatitudeCoord()
        min_max_longitude_coord = self.getMinMaxLongitudeCoord()

        self.top_right_corner = (min_max_latitude_coord[1], min_max_longitude_coord[1]) # lat long coords
        self.bottom_left_corner = (min_max_latitude_coord[0], min_max_longitude_coord[0])

    def latLongToPixel(self, lat, long):
        getcontext().prec = 10
        lat = Decimal(str(lat))
        long = Decimal(str(long))

        scale = Decimal(c.TILE_SIZE) * Decimal(2)**Decimal(c.ZOOM)

        long_x = (long + Decimal(180)) / Decimal(360) * scale

        sin_lat = math.sin(math.radians(float(lat))) # Decimal not supported for math
        lat_y = (Decimal(0.5) - Decimal(math.log((1 + sin_lat) / (1 - sin_lat))) / (Decimal(4) * Decimal(math.pi))) * scale

        return (lat_y, long_x)
    
    def pixelToLatLong(self, y, x):
        getcontext().prec = 10
        scale = Decimal(c.TILE_SIZE) * Decimal(2)**Decimal(c.ZOOM)

        long = (Decimal(str(x)) / scale) * Decimal(360) - Decimal(180)

        n = Decimal(math.pi) - (Decimal(2) * Decimal(math.pi) * Decimal(str(y)) / scale)
        lat_rad = math.atan(math.sinh(float(n)))  # Decimal not supported for math
        lat = Decimal(str(math.degrees(lat_rad)))

        return (self.roundDecimal(lat), self.roundDecimal(long))
    
    def getPixelDistanceFromLatLongCoords(self, lat_long_1, lat_long_2):
        lat_y_1, long_x_1 = self.latLongToPixel(lat_long_1[0], lat_long_1[1])
        lat_y_2, long_x_2 = self.latLongToPixel(lat_long_2[0], lat_long_2[1])

        width = abs(long_x_2 - long_x_1)
        height = abs(lat_y_2 - lat_y_1)

        print({'width': self.roundDecimal(width, ROUND_UP, 0), 'height': self.roundDecimal(height, ROUND_UP, 0)})
        return {'width': self.roundDecimal(width, ROUND_UP, 0), 'height': self.roundDecimal(height, ROUND_UP, 0)}

    def roundDecimal(self, num, rounding=ROUND_HALF_UP, places=6):
        precision = Decimal("1").scaleb(-int(places))
        return num.quantize(precision, rounding)
    
    def computeBandsShiftsNumber(self):
        #get pixel distance from rectangle, top and left side
        # divide by viewport size -> number of shifts and number of bands
        # get pixel xy from left edge of the rectangle -> beginnings of bands
        # convert pixel beginnings to lat long coords
        # save to list
        print('top right ', self.top_right_corner)
        print('bottom left ', self.bottom_left_corner)
        top_left_corner = (self.top_right_corner[0], self.bottom_left_corner[1]) # lat long
        print('top left ', top_left_corner)
        rectangle_width = self.getPixelDistanceFromLatLongCoords(top_left_corner, self.top_right_corner)['width'] + c.MAP_WIDTH #decimal type

        rectangle_height = self.getPixelDistanceFromLatLongCoords(top_left_corner, self.bottom_left_corner)['height'] + c.MAP_HEIGHT # decimal type
        print('height ', rectangle_height)
        print('width ', rectangle_width)

        number_bands = int(self.roundDecimal(rectangle_height / c.MAP_HEIGHT, ROUND_UP, 0))
        number_shifts = int(self.roundDecimal(rectangle_width / c.MAP_WIDTH, ROUND_UP, 0))
        print('number bands ', number_bands)
        print('number_shifts ', number_shifts)

        top_left_pixel = self.latLongToPixel(top_left_corner[0], top_left_corner[1])
        print("type: ", type(top_left_pixel[0]))
        print(type(top_left_pixel[1]))

        print(self.pixelToLatLong(top_left_pixel[0], top_left_pixel[1]))

        for band in range(number_bands):
            starting_coords = (top_left_pixel[0] + c.MAP_HEIGHT*band, top_left_pixel[1])
            print('left corner ', top_left_corner)
            print('starting coords ', starting_coords)
            # lat_y_rounded = self.roundDecimal(starting_coords[0], places=0)
            # long_x_rounded = self.roundDecimal(starting_coords[1], places=0)
            lat_long = self.pixelToLatLong(starting_coords[0], starting_coords[1])
            # lat_long = self.pixelToLatLong(lat_y_rounded, long_x_rounded)
            self.area.append([lat_long, number_shifts])

        print(self.area)





