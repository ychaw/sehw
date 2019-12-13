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

        WebDriverWait(driver, 10).until(e_c.presence_of_element_located((By.CLASS_NAME, 'options-header')))
        self.assertIn('https://app.numidian.io/convert/', driver.current_url)

        WebDriverWait(driver, 10).until(e_c.presence_of_element_located((By.CLASS_NAME, 'records')))

        # find the text input and replace abc with column
        
        # this sometimes misses the first two inputs, make the selector more explicit

        for i in range(1, 5):
            
            css_selector = "div:nth-child(§) .form-field:nth-child(2) > .input".replace("§", str(i))
            field = driver.find_element(By.CSS_SELECTOR, css_selector)
            field.clear()
            field.send_keys("column_" + str(i))
            updatedText = driver.find_element(By.CSS_SELECTOR, css_selector).get_attribute("value")
            self.assertIn('column_', updatedText) # check if changing the text worked
            self.assertNotIn('abc', updatedText)
        
        # find and click export button

        exportButton = driver.find_element_by_xpath("//div[@class='text-right']/button")
        exportButton.click()

        # wait until the export window is open and visible

        WebDriverWait(driver, 5).until(e_c.visibility_of_element_located((By.CLASS_NAME, 'modal-content')))
        pop_up_window = driver.find_element_by_css_selector('.modal-content')
        
        heading = pop_up_window.find_element_by_class_name('modal-title')
        self.assertIn('Export your data', heading.text)
        
        # click the export button

        export_file_button = pop_up_window.find_element_by_class_name('btn-primary')
        export_file_button.click()

        # check if "Export completed" is in popup

        WebDriverWait(driver, 40).until(e_c.presence_of_element_located((By.CSS_SELECTOR, '.alert-ok')))
        self.assertIn('Export completed', pop_up_window.text)

        # Download button is clickable
        downloadButtonSelector = ".modal-content .btn-okay" # this one probably doesn't work
        WebDriverWait(driver, 10).until(e_c.element_to_be_clickable((By.CSS_SELECTOR, downloadButtonSelector)))
        downloadButton = driver.find_element_by_css_selector(downloadButtonSelector)
        downloadButton.click()

        downloadDialog = driver.switch_to_alert()

        #adjust file path depending on os
        pathToDownloadFolder = ""
        if os.uname().sysname == 'Linux':
            pathToDownloadFolder = os.path.expanduser("~/Downloads/")
        else:   
            pathToDownloadFolder = os.path.expanduser("~user\\Downloads\\")  # CHECK this please
        
        pathToFile = pathToDownloadFolder + "document_1.json"
        downloadDialog.send_keys(pathToFile)
        downloadDialog.submit()

        # File is in ~/Downloads (unix) or user\Downloads (windows)
        self.assertTrue(os.path.isfile(pathToFile))

        # for input_col_name in driver.find_elements_by_xpath("//input[@placeholder='id']"):
        #     print(input_col_name.text)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
