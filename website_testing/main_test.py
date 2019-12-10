import time
import os

import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("https://sqlify.io/")
        convert_button = driver.find_element_by_class_name('btn-primary')
        convert_button.click()
        drop_area = driver.find_element_by_class_name('drop-area')
        input_file = drop_area.find_element_by_id('file')
        input_file.send_keys(os.getcwd() + '\\data\\document_1.csv')

        self.assertIn('document_1.csv', drop_area.text)

        upload_button = driver.find_element_by_class_name('convert-button')
        upload_button.click()

        WebDriverWait(driver, 5).until(e_c.presence_of_element_located((By.CLASS_NAME, 'options-header')))
        self.assertIn('https://app.sqlify.io/convert/', driver.current_url)

        # fields = driver.find_element_by_class_name('fields')

        for input_col_name in driver.find_elements_by_xpath("//input[@placeholder='id']")):
            print(input_col_name.text)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
