from enum import Enum


class SeleniumBrowser(Enum):
    FIREFOX_BROWSER = 'firefox'
    CHROME_BROWSER = 'chrome'


class SeleniumMode(Enum):
    HEADLESS_MODE_ON = 'on'
    HEADLESS_MODE_OFF = 'off'
