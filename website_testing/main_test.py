import time
import os

import unittest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.dir", os.path.join(os.getcwd(), 'downloads'))
        # profile.set_preference("browser.download.manager.showWhenStarting", False)
        # profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/json")
        # profile.set_preference("browser.download.manager.closeWhenDone", False)
        # profile.set_preference("browser.download.manager.focusWhenStarting", False)

        self.driver = webdriver.Firefox(profile)

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("https://numidian.io/")
        convert_button = driver.find_element_by_class_name('btn-neutral')
        convert_button.click()
        drop_area = driver.find_element_by_class_name('drop-area')
        input_file = drop_area.find_element_by_id('file')

        #adjust file path depending on os
        input_file.send_keys(os.path.join(os.getcwd(),'data', 'document_1.csv'))
        
        WebDriverWait(driver, 5).until(e_c.text_to_be_present_in_element((By.CLASS_NAME, 'drop-area'), 'document'))
        self.assertIn('document_1.csv', drop_area.text)

        upload_button = driver.find_element_by_class_name('btn-primary.big')
        upload_button.click()

        WebDriverWait(driver, 10).until(e_c.presence_of_element_located((By.CLASS_NAME, 'options-header')))
        self.assertIn('https://app.numidian.io/convert/', driver.current_url)

        WebDriverWait(driver, 10).until(e_c.presence_of_element_located((By.CLASS_NAME, 'records')))

        # find the text input and replace abc with column
        
        # this sometimes misses the first two inputs, make the selector more explicit

        for input_col_name in driver.find_elements_by_xpath("//input[@placeholder='id']"):
            new_text = input_col_name.get_attribute('value').replace('abc', 'column')
            input_col_name.clear()
            input_col_name.send_keys(new_text)
        
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

        
        path_to_downloaded_file = os.path.join(os.getcwd(), 'downloads')
        list_of_jsons = [os.path.join(path_to_downloaded_file, f) for f in os.listdir(path_to_downloaded_file) if f.endswith('.json')]

        # Download button is clickable
        download_button_xpath = "//span[@class='margin-left-auto']/a"
        WebDriverWait(driver, 10).until(e_c.element_to_be_clickable((By.XPATH, download_button_xpath)))
        download_button = driver.find_element_by_xpath(download_button_xpath)
        download_button.click()


        # SAVE FILE MANUALLY

        # neither selenium alerts or firefox profile preferences are working for me


        # File is in Download Folder
        new_list_of_jsons = [os.path.join(path_to_downloaded_file, f) for f in os.listdir(path_to_downloaded_file) if f.endswith('.json')]
        self.assertTrue(len(list_of_jsons) != len(new_list_of_jsons))

        json_file = open([d for d in new_list_of_jsons if d not in list_of_jsons][0])
        csv_file = open(os.path.join(os.getcwd(),'data', 'document_1.csv'))
        json_file = open([d for d in new_list_of_jsons][0])
        print()
        print(csv_file.read())
        print()
        print(json_file.read())
        print()


    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
