import time
import os

import unittest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from website_testing.selenium_utils.selenium_test_case import SeleniumTestCase


class FileConversion(SeleniumTestCase):

    def setUp(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.dir", os.path.join(os.getcwd(), 'downloads'))
        # profile.set_preference("browser.download.manager.showWhenStarting", False)
        # profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/json")
        # profile.set_preference("browser.download.manager.closeWhenDone", False)
        # profile.set_preference("browser.download.manager.focusWhenStarting", False)

        self.driver = webdriver.Firefox(profile)
        self.start_page.navigate()

    def test_file_conversion(self):
        # driver = self.driver
        # driver.get("https://numidian.io/")
        # convert_button = driver.find_element_by_class_name('btn-neutral')
        # convert_button.click()

        #adjust file path depending on os
        file_path = os.path.join(os.getcwd(),'data', 'document_1.csv')
        self.start_page.upload_file(file_path)
        self.assertIn('document_1.csv', self.start_page.get_drop_area().text)

        self.start_page.click_upload_button()
        self.assertIn('https://app.numidian.io/convert/', self.start_page.driver_proxy.driver.current_url)
        
        self.convert_page.wait_until_data_is_loaded()

        # find the text input and replace abc with column
        self.convert_page.replace_column_names()
               
        # find and click export button
        self.convert_page.click_export_button()

        # wait until the export window is open and visible
        self.convert_page.wait_for_pop_up()
        self.assertIn('Export your data', self.convert_page.get_popup_heading.text)
        
        # click the export button
        self.convert_page.click_confirm_export_button()

        # check if "Export completed" is in popup
        self.convert_page.wait_for_export()
        self.assertIn('Export completed', self.convert_page.get_pop_up().text)

        
        path_to_downloaded_file = os.path.join(os.getcwd(), 'downloads')
        list_of_jsons = [os.path.join(path_to_downloaded_file, f) for f in os.listdir(path_to_downloaded_file) if f.endswith('.json')]

        # click Download button if clickable
        self.convert_page.click_download_button()

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
