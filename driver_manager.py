import consts as c

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class DriverManager:
    def __init__(self):
        self.driver = None

    def launchCromeWithSelenium(self, x_start=c.X_START, y_start=c.Y_START, zoom=c.ZOOM, no_overlays=True):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        self.driver.set_window_size(1200, 800)  #viewport size
        self.driver.get(c.URL.format(zoom=zoom, x=x_start, y=y_start))

        if(no_overlays):
            self.hideElements(c.OVERLAY_ELEMENTS_CLASSES)
    
    def injectScript(self, script, *vars_to_return):
        self.driver.execute_script(script)

        input("Press Enter to exit and close the browser...")

        data = []
        for var in vars_to_return:
            data.append(self.driver.execute_script(f"return window.{var}"))
        
        return data
    
    def hideElements(self, classesString):
        self.driver.execute_script(f"""
            document.querySelectorAll('{classesString}').forEach(e => e.style.display = 'none');
        """)

    def getDriver(self):
        return self.driver
    
    def closeDriver(self):
        self.driver.quit()
        self.driver = None
