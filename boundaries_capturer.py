from driver_manager import DriverManager as DM
from consts import BOUNDARIES_SCRIPT

class BoundariesCapturer:
    def __init__(self):
        pass

    def getPoints(self):
        DM.launchCromeWithSelenium()
        points = DM.injectScript(BOUNDARIES_SCRIPT, 'boundaryPoints')
        DM.closeDriver()
        return points
    
    def formatPoints(self):
        pass