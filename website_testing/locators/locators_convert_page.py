from typing import Tuple

from selenium.webdriver.common.by import By


class ConvertPageLocators(object):
    """A class for upload page locators. All upload page locators should come here"""
    RECORDS: Tuple[str, str] = (By.CLASS_NAME, 'records')
    COLUMN_NAMES: Tuple[str, str] = (By.XPATH, "//input[@placeholder='id']")
    EXPORT_BUTTON: Tuple[str, str] = (By.XPATH, "//div[@class='text-right']/button")
    POP_UP_WINDOW: Tuple[str, str] = (By.CLASS_NAME, "modal-content")
    EXPORT_CONFIRMATION: Tuple[str, str] = (By.CSS_SELECTOR, '.alert-ok')
    DOWNLOAD_BUTTON: Tuple[str, str] = (By.XPATH, "//span[@class='margin-left-auto']/a")
    