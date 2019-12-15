from abc import ABC, abstractmethod
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from website_testing.selenium_utils.driver_proxy import DriverProxy
from website_testing.locators.locators_base_page import BasePageLocators


class BasePage(ABC):
    """Base class to initialize the base page.
     It provides general interactions for all pages"""

    def __init__(self, driver_proxy: DriverProxy):
        self.driver_proxy = driver_proxy

    base_url = "https://numidian.io"

    @abstractmethod
    def navigate(self):
        """Navigates to the page's url"""

    def refresh(self):
        self.driver_proxy.driver.refresh()

    def click_button(self, element, duration):
        """
        Click a button tag, which is clickable within a given duration
        :param element: selenium locator
        :param duration: Time period within the element must be clickable (in seconds)
        :return:
        """
        wait = WebDriverWait(self.driver_proxy.driver, duration)
        button = wait.until(EC.element_to_be_clickable(element))
        button.click()

    def get_menu_bar(self, duration):
        wait = WebDriverWait(self.driver_proxy.driver, duration)
        return wait.until(EC.visibility_of_element_located(BasePageLocators.MENU_BAR))

    def click_menu_item_pricing(self, duration):
        menu_bar = self.get_menu_bar(duration)
        menu_item = menu_bar.find_elements_by_tag_name("li")[2]
        menu_item.find_element_by_tag_name("a").click()
