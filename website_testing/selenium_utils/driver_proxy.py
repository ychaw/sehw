import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

from website_testing.config import config
from website_testing.selenium_utils import selenium_config


class DriverProxy:
    """
    This class encapsulates a selenium WebDriver.
    Basically it is used to instantiate a WebDriver recognizing
    the configurations made in AI_Matching_Box.config and as a Proxy.
    """

    default_browser_type = config['selenium']['browser']
    default_mode = config['selenium']['headless_mode']
    FILE_DIR = os.path.dirname(__file__)
    TEST_DIRCTORY = os.path.dirname(FILE_DIR)

    def __init__(self, browser_type=default_browser_type, mode=default_mode):
        self.browser_type = browser_type
        self.mode = mode
        self.driver = self._create_driver()

    def _create_driver(self):
        """
        :return: a WebDriver instance created regarding settings in config.py
        """
        driver = None

        if self.browser_type == selenium_config.SeleniumBrowser.FIREFOX_BROWSER:
            # get path of driver file
            fire_fox_driver_path = self.TEST_DIRCTORY + "/driver_files/geckodriver.exe"

            # adjust if linux
            if os.uname().sysname == 'Linux':
                fire_fox_driver_path = self.TEST_DIRCTORY + "/driver_files/geckodriver"

            # Set some options for driver
            options = FirefoxOptions()
            options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
            options.add_argument("--no-sandbox")  # Bypass OS security model

            # Depending on the setting of the entry in config.py the headless mode is on or off
            if self.mode == selenium_config.SeleniumMode.HEADLESS_MODE_ON:
                options.headless = True
            elif self.mode == selenium_config.SeleniumMode.HEADLESS_MODE_ON:
                options.headless = False

            # Create a new instance of the Firefox driver
            driver = webdriver.Firefox(executable_path=fire_fox_driver_path,
                                       options=options)

        elif self.browser_type == selenium_config.SeleniumBrowser.CHROME_BROWSER:
            # get path of driver file
            chrome_driver_path = self.TEST_DIRCTORY + "/driver_files/chromedriver.exe"

            # adjust if linux
            if os.uname().sysname == 'Linux':
                chrome_driver_path = self.TEST_DIRCTORY + "/driver_files/chromedriver"

            # Set some options for driver
            options = ChromeOptions()
            options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
            options.add_argument("--no-sandbox")  # Bypass OS security model

            # Depending on the setting of the entry in config.py the headless mode is on or off
            if self.mode == selenium_config.SeleniumMode.HEADLESS_MODE_ON:
                options.headless = True
            elif self.mode == selenium_config.SeleniumMode.HEADLESS_MODE_OFF:
                options.headless = False

            # Create a new instance of the Chrome driver
            driver = webdriver.Chrome(chrome_driver_path, options=options)

        return driver
