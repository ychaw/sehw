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

        columnNameFieldLocatorXPATH = "//div[@class='form-field']/input[@placeholder='id']"
        columnNameFields = driver.find_elements(By.XPATH, columnNameFieldLocatorXPATH)
        
        for field in columnNameFields:
            old_text = field.get_attribute("value")
            print(old_text)
            self.assertIn('abc_', old_text)
            field.clear()
            field.send_keys(old_text.replace('abc', 'column'))

            updatedText = field.get_attribute("value")
            self.assertIn('column_', updatedText) # check if changing the text worked
            self.assertNotIn('abc', updatedText)

        # find the export button
        
        # I copied this path out of the page with devtools, but it also doesn't work, 
        # so there must be another issue somewhere
        # exportButton = driver.find_element_by_xpath("/html/body/div/div/div[2]/header/div[3]/button")
        
        exportButton = driver.find_element_by_xpath("//div[@class='text-right']/button") # doesn't find the element
        exportButton.click()

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
