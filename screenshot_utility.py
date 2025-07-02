from driver_manager import DriverManager as DM

class ScreenshotUtility:
    def __init__(self):
        pass

    def makeScreenshots(self):
        DM.launchChromeWithSelenium()
        