import consts as c

from decimal import Decimal, getcontext, ROUND_HALF_UP, ROUND_UP
import math
import os
import json

class TilesCreator:
    """
    Processes all the latitude and longitude coordinates collected by user. Locates corners of the rectangluar map.
    Divides rectangular area into tiles and stores their coordinates for future screenshot making.

     Attributes:
        map_coords (list): Contains two-element tuples with strings, (lat, long)
        area (list): Contains lists with a two-element tuple and an integer, [(lat, long), number]
    """

    def __init__(self):
        self.map_coords = []
        self.area = []

    def convert_to_decimal(self):
        self.map_coords = [(Decimal(lat), Decimal(long)) for lat, long in self.map_coords]

    def read_map_coords(self, map_title=None):
        with open(os.path.join(c.BOUNDARIES_OUTPUT_FOLDER, f"{map_title if map_title else c.map_title}.json"), "r") as boundaries_storage:
            json_all = json.load(boundaries_storage)
            map_coords_as_lists = json_all["data"]
            self.map_coords = [tuple(coords) for coords in map_coords_as_lists]

    def get_min_max_longitude_coord(self):
        _, long = zip(*self.map_coords)
        return (min(long), max(long))

    def get_min_max_latitude_coord(self):
        lat, _ = zip(*self.map_coords)
        return (min(lat), max(lat))
    
    def get_container_rectangle(self):
        min_max_latitude_coord = self.get_min_max_latitude_coord()
        min_max_longitude_coord = self.get_min_max_longitude_coord()

        self.top_right_corner = (min_max_latitude_coord[1], min_max_longitude_coord[1]) # lat long coords
        self.bottom_left_corner = (min_max_latitude_coord[0], min_max_longitude_coord[0])

    def lat_long_to_pixel(self, lat, long):
        getcontext().prec = 10
        lat = Decimal(str(lat))
        long = Decimal(str(long))

        scale = Decimal(c.TILE_SIZE) * Decimal(2)**Decimal(c.zoom)

        long_x = (long + Decimal(180)) / Decimal(360) * scale

        sin_lat = math.sin(math.radians(float(lat))) # Decimal not supported for math
        lat_y = (Decimal(0.5) - Decimal(math.log((1 + sin_lat) / (1 - sin_lat))) / (Decimal(4) * Decimal(math.pi))) * scale

        return (lat_y, long_x)
    
    def pixel_to_lat_long(self, y, x):
        getcontext().prec = 10
        scale = Decimal(c.TILE_SIZE) * Decimal(2)**Decimal(c.zoom)

        long = (Decimal(str(x)) / scale) * Decimal(360) - Decimal(180)

        n = Decimal(math.pi) - (Decimal(2) * Decimal(math.pi) * Decimal(str(y)) / scale)
        lat_rad = math.atan(math.sinh(float(n)))  # Decimal not supported for math
        lat = Decimal(str(math.degrees(lat_rad)))

        return (self.round_decimal(lat), self.round_decimal(long))
    
    def get_pixel_distance_from_lat_long_coords(self, lat_long_1, lat_long_2):
        lat_y_1, long_x_1 = self.lat_long_to_pixel(lat_long_1[0], lat_long_1[1])
        lat_y_2, long_x_2 = self.lat_long_to_pixel(lat_long_2[0], lat_long_2[1])

        width = abs(long_x_2 - long_x_1)
        height = abs(lat_y_2 - lat_y_1)

        return {'width': self.round_decimal(width, ROUND_UP, 0), 'height': self.round_decimal(height, ROUND_UP, 0)}

    def round_decimal(self, num, rounding=ROUND_HALF_UP, places=6):
        precision = Decimal("1").scaleb(-int(places))
        return num.quantize(precision, rounding)
    
    def compute_bands_shifts_number(self):
        top_left_corner = (self.top_right_corner[0], self.bottom_left_corner[1]) # lat long
        rectangle_width = self.get_pixel_distance_from_lat_long_coords(top_left_corner, self.top_right_corner)['width'] + c.map_width #decimal type
        rectangle_height = self.get_pixel_distance_from_lat_long_coords(top_left_corner, self.bottom_left_corner)['height'] + c.map_height # decimal type

        number_bands = int(self.round_decimal(rectangle_height / c.map_height, ROUND_UP, 0))
        number_shifts = int(self.round_decimal(rectangle_width / c.map_width, ROUND_UP, 0))-1

        top_left_pixel = self.lat_long_to_pixel(top_left_corner[0], top_left_corner[1])

        for band in range(number_bands):
            starting_coords = (top_left_pixel[0] + c.map_height*band, top_left_pixel[1])
            lat_y_rounded = self.round_decimal(starting_coords[0], places=0)
            long_x_rounded = self.round_decimal(starting_coords[1], places=0)
            lat_long = self.pixel_to_lat_long(lat_y_rounded, long_x_rounded)
            self.area.append([lat_long, number_shifts])




