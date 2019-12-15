from typing import Tuple

from selenium.webdriver.common.by import By


class StartPageLocators(object):
    """A class for upload page locators. All upload page locators should come here"""
    DROP_AREA: Tuple[str, str] = (By.CLASS_NAME, "drop-area")
    UPLOAD_BUTTON: Tuple[str, str] = (By.CLASS_NAME, "btn-primary.big")
    OPTIONS_HEADER: Tuple[str, str] = (By.CLASS_NAME, 'options-header')