import unittest
import time

from website_testing.selenium.selenium_utils.selenium_test_case import SeleniumTestCase


class ExampleCase(SeleniumTestCase):
    """
    Place explanation of test journey here.
    """
    def setup_journey(self):
        self.start_page.navigate()

    def redirect_pricing_page(self):
        """
        Place explanation of test method here.
        """
        # Act
        self.start_page.click_menu_item_pricing(duration=10)
        time.sleep(4)

        # Assert
        expected_url = "https://sqlify.io/pricing"
        current_url = self.driver_proxy.driver.current_url
        self.assertEqual(expected_url, current_url)

    def test_journey(self):
        # Arrange
        self.setup_journey()

        # 1. Step
        self.redirect_pricing_page()


if __name__ == '__main__':
    unittest.main()
