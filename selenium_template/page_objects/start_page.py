from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from website_testing.selenium.page_objects.base_page import BasePage
from website_testing.selenium.locators.locators_start_page import StartPageLocators


class StartPage(BasePage):
    """
    This class contains methods for interacting with and navigating
    through the start page.
    """

    endpoint = "/"   # you have to change it!

    def navigate(self):
        self.driver_proxy.driver.get(self.base_url + self.endpoint)
