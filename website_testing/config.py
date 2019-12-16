from website_testing.selenium_utils.selenium_config import SeleniumBrowser, SeleniumMode

config: dict = {
    'selenium': {
        'browser': SeleniumBrowser.FIREFOX_BROWSER,
        'headless_mode': SeleniumMode.HEADLESS_MODE_OFF,
    }
}
