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
        driver.get("https://numidian.io/")
        convert_button = driver.find_element_by_class_name('btn-neutral')
        convert_button.click()
        drop_area = driver.find_element_by_class_name('drop-area')
        input_file = drop_area.find_element_by_id('file')

        #adjust file path depending on os
        if os.uname().sysname == 'Linux':
            input_file.send_keys(os.getcwd() + '/data/document_1.csv')
        else:    
            input_file.send_keys(os.getcwd() + '\\data\\document_1.csv')
        
        WebDriverWait(driver, 5).until(e_c.text_to_be_present_in_element((By.CLASS_NAME, 'drop-area'), 'document'))
        self.assertIn('document_1.csv', drop_area.text)

        upload_button = driver.find_element_by_class_name('btn-primary.big')
        upload_button.click()

        WebDriverWait(driver, 5).until(e_c.presence_of_element_located((By.CLASS_NAME, 'options-header')))
        self.assertIn('https://app.numidian.io/convert/', driver.current_url)


        # find the text input and replace abc with column

        fields = driver.find_elements_by_class_name('field')
        for field in fields:
            column_name_input = field.find_element_by_xpath("/div[@class='form-field']/input[2]") # doesn't work
            old_text = column_name_input.text
            self.assertIn('abc_', old_text) # sometimes doesn't work
            column_name_input.clear()
            column_name_input.send_keys(old_text.replace('abc', 'column'))

        # check if changing the text worked

        for field in driver.find_elements_by_class_name('field'):
            column_name = field.find_elements_by_class_name("form-field")[1]
            text_input = column_name.find_element_by_tag_name("input")
            self.assertIn('column_', text_input.text)
            self.assertNotIn('abc', text_input.text)

        # find the export button

        buttons = driver.find_elements_by_xpath("//*[@class='btn-primary extra-small']") # doesn't work, returns empty
        for button in buttons:
            button.click()

        # wait until the export window is open and visible

        WebDriverWait(driver, 5).until(e_c.visibility_of_element_located((By.CLASS_NAME, 'modal-content')))
        pop_up_window = driver.find_element_by_css_selector('.modal-content')
        
        heading = pop_up_window.find_element_by_class_name('modal-title')
        self.assertIn('Export your data', heading.text)
        
        # click the export button

        export_file_button = pop_up_window.find_element_by_class_name('btn-primary')
        export_file_button.click()

        WebDriverWait(driver, 5).until(e_c.presence_of_element_located((By.CLASS_NAME, 'alert-ok')))
        self.assertIn('Export completed', pop_up_window.text)

        

        # for input_col_name in driver.find_elements_by_xpath("//input[@placeholder='id']"):
        #     print(input_col_name.text)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
