from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from website_testing.page_objects.base_page import BasePage
from website_testing.locators.locators_convert_page import ConvertPageLocators


class ConvertPage(BasePage):
    """
    This class contains methods for interacting with and navigating
    through the conversion page.
    """

    def wait_until_data_is_loaded(self):
        WebDriverWait(self.driver_proxy.driver, 10).until(EC.presence_of_element_located((ConvertPageLocators.RECORDS)))

    def replace_column_names(self):
        for input_col_name in self.driver_proxy.driver.find_elements(ConvertPageLocators.COLUMN_NAMES):
                new_text = input_col_name.get_attribute('value').replace('abc', 'column')
                input_col_name.clear()
                input_col_name.send_keys(new_text)

    def click_export_button(self):
        self.click_button(ConvertPageLocators.EXPORT_BUTTON, 5)

    def get_popup_heading(self):
        pop_up_window = self.driver_proxy.driver.find_elements(ConvertPageLocators.POP_UP_WINDOW)
        return pop_up_window.find_element_by_class_name('modal-title')

    def wait_for_pop_up(self):
        return WebDriverWait(self.driver_proxy.driver, 5).until(EC.visibility_of_element_located(ConvertPageLocators.POP_UP_WINDOW))

    def get_pop_up(self):
        return self.driver_proxy.driver.find_element(ConvertPageLocators.POP_UP_WINDOW)

    def click_confirm_export_button(self):
        pop_up_window = self.get_pop_up()
        export_file_button = pop_up_window.find_element_by_class_name('btn-primary')
        export_file_button.click()

    def wait_for_export(self):
        WebDriverWait(self.driver_proxy.driver, 40).until(EC.presence_of_element_located(ConvertPageLocators.EXPORT_CONFIRMATION))

    def click_download_button(self):
        WebDriverWait(self.driver_proxy.driver, 10).until(EC.element_to_be_clickable(ConvertPageLocators.DOWNLOAD_BUTTON))
        self.click_button(ConvertPageLocators.DOWNLOAD_BUTTON, 5)
        