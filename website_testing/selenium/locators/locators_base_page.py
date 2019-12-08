from typing import Tuple

from selenium.webdriver.common.by import By


class BasePageLocators(object):
    """A class for base page locators. All base page locators should come here"""

    # Menu Bar in Header
    MENU_BAR: Tuple[str, str] = (By.CLASS_NAME, "menu")

