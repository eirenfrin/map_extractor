import consts as c

from decimal import Decimal, getcontext, ROUND_HALF_UP
import math

class TilesCreator:
    def __init__(self, map_coords):
        self.map_coords = map_coords # list of (lat, long) tuples

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

        return (long_x, lat_y)
    
    def pixelToLatLong(self, x, y):
        scale = Decimal(c.TILE_SIZE) * Decimal(2)**Decimal(c.ZOOM)

        long = (Decimal(x) / scale) * Decimal(360) - Decimal(180)

        n = Decimal(math.pi) - (Decimal(2) * Decimal(math.pi) * Decimal(y) / scale)
        lat_rad = math.atan(math.sinh(float(n)))  # Decimal not supported for math
        lat = Decimal(str(math.degrees(lat_rad)))

        return (self.roundDecimal(long), self.roundDecimal(lat))
    
    def getPixelDistanceFromLatLongCoords(self, lat_long_1, lat_long_2):
        long_x_1, lat_y_1 = self.latLongToPixel(lat_long_1[0], lat_long_1[1])
        long_x_2, lat_y_2 = self.latLongToPixel(lat_long_2[0], lat_long_2[1])

        width = long_x_2 - long_x_1
        height = lat_y_2 - lat_y_1

        return {'width': width, 'height': height}

    def roundDecimal(self, num, places=6):
        precision = Decimal("1").scaleb(-int(places))
        return num.quantize(precision, rounding=ROUND_HALF_UP)