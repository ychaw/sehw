from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from website_testing.page_objects.base_page import BasePage
from website_testing.locators.locators_start_page import StartPageLocators


class StartPage(BasePage):
    """
    This class contains methods for interacting with and navigating
    through the start page.
    """

    endpoint = "/convert"   # you have to change it!

    def navigate(self):
        self.driver_proxy.driver.get(self.base_url + self.endpoint)

    def get_drop_area(self):
        return self.driver_proxy.driver.find_element(StartPageLocators.DROP_AREA)

    def get_file_input(self):
        drop_area = self.get_drop_area()
        return drop_area.find_element_by_id('file')
    
    def upload_file(self, file_path):
        file_input = self.get_file_input()
        file_input.send_keys(file_path)
        WebDriverWait(self.driver_proxy.driver, 5).until(EC.text_to_be_present_in_element((StartPageLocators.DROP_AREA), 'document'))

    def click_upload_button(self):
        self.click_button(StartPageLocators.UPLOAD_BUTTON, 5)
        WebDriverWait(self.driver_proxy.driver, 10).until(EC.presence_of_element_located((StartPageLocators.OPTIONS_HEADER)))

