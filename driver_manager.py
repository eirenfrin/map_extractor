import consts as c
from utils import default_to_constant

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class DriverManager:
    """
    Opens a new Chrome window and performs all driver actions.

     Attributes:
        driver (WebDriver): Holds current instance of web driver
    """

    def __init__(self):
        self.driver = None

    @default_to_constant({'zoom': 'zoom'})
    def launch_chrome_with_selenium(self, x_start=c.X_START, y_start=c.Y_START, zoom=None, no_overlays=True, show_window=True):
        options = Options()
        if not show_window:
            options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)

        self.driver.set_window_size(c.window_width, c.window_height)
        self.driver.get(c.URL.format(zoom=zoom, x=x_start, y=y_start))

        if(no_overlays):
            self.hide_elements(c.OVERLAY_ELEMENTS_CLASSES)
    
    def inject_script(self, script, wait=False):
        self.driver.execute_script(script)

        if wait:
            input("Press Enter to exit and close the browser...")
    
    def poll_for_variables(self, var, *more_vars):
        data = [self.driver.execute_script(f"return window.{var}")]

        for var in more_vars:
            data.append(self.driver.execute_script(f"return window.{var}"))

        return data if more_vars else data[0]
    
    def hide_elements(self, classes_string):
        self.driver.execute_script(f"""
            document.querySelectorAll('{classes_string}').forEach(e => e.style.display = 'none');
        """)

    def get_driver(self):
        return self.driver
    
    def get_map_element(self):
        return self.driver.find_element(By.CLASS_NAME, c.MAP_CONTAINER_CLASSES)
    
    def close_driver(self):
        self.driver.quit()
        self.driver = None
