from website_testing.selenium.selenium_utils.selenium_config import SeleniumBrowser, SeleniumMode

config: dict = {
    'selenium': {
        'browser': SeleniumBrowser.CHROME_BROWSER,
        'headless_mode': SeleniumMode.HEADLESS_MODE_OFF,
    }
}
