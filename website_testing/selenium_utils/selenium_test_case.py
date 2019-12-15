import unittest
from pathlib import Path

from website_testing.page_objects.start_page import StartPage
from website_testing.page_objects.convert_page import ConvertPage
from website_testing.selenium_utils.driver_proxy import DriverProxy


class SeleniumTestCase(unittest.TestCase):
    test_folder = str(Path(__file__).parents[1])
    assets_folder = test_folder + '/assets/'
    driver_proxy = None
    start_page = None
    convert_page = None
    # Add further page objects here

    @classmethod
    def setUpClass(cls):
        cls.driver_proxy = DriverProxy()
        cls.driver_proxy.driver.set_window_size(1920, 1080)
        cls.start_page: StartPage = StartPage(cls.driver_proxy)
        cls.convert_page: ConvertPage = ConvertPage(cls.driver_proxy)
        # Initialise page objects here

    @classmethod
    def tearDownClass(cls):
        cls.driver_proxy.driver.close()

