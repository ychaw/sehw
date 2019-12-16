import time
import sys
import os

import csv
import json

import unittest

# So I don't have to reset my PATH everytime and all modules can be imported
sys.path.append(os.path.dirname(os.getcwd()))

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from website_testing.selenium_utils.selenium_test_case import SeleniumTestCase

class FileConversion(SeleniumTestCase):

    def setUp(self):
        self.start_page.navigate()

    def test_file_conversion(self):
        test_documents=['document_1.csv', 'document_2.csv']
        for f in test_documents:
            self.conversion_journey(f)

    def conversion_journey(self, test_file):
        
        self.start_page.navigate()

        #adjust file path depending on os
        csv_file_path = os.path.join(os.getcwd(),'assets', test_file)
        self.start_page.upload_file(csv_file_path)
        self.assertIn(test_file, self.start_page.get_drop_area().text)

        self.start_page.click_upload_button()
        self.assertIn('https://app.numidian.io/convert/', self.start_page.driver_proxy.driver.current_url)
        
        self.convert_page.wait_until_data_is_loaded()

        # find the text input and replace abc with column
        self.convert_page.replace_column_names()
               
        # find and click export button
        self.convert_page.click_export_button()

        # wait until the export window is open and visible
        self.convert_page.wait_for_pop_up()
        self.assertIn('Export your data', self.convert_page.get_popup_heading().text)
        
        # click the export button
        self.convert_page.click_confirm_export_button()

        # check if "Export completed" is in popup
        self.convert_page.wait_for_export()
        self.assertIn('Export completed', self.convert_page.get_pop_up().text)

        path_to_downloaded_file = os.path.join(os.path.expanduser("~"), "Downloads")
        list_of_jsons = [os.path.join(path_to_downloaded_file, f) for f in os.listdir(path_to_downloaded_file) if f.endswith('.json')]

        # click Download button if clickable
        self.convert_page.click_download_button()

        # SAVE FILE MANUALLY
        # neither selenium alerts or firefox profile preferences are working for me
        self.convert_page.wait_for(30)


        # File is in Download Folder
        new_list_of_jsons = [os.path.join(path_to_downloaded_file, f) for f in os.listdir(path_to_downloaded_file) if f.endswith('.json')]
        self.assertTrue(len(list_of_jsons) != len(new_list_of_jsons))

        # Get the new json file we just downloaded
        jsons_to_test_against = [f for f in filter(lambda el: el not in list_of_jsons, new_list_of_jsons)]
        
        csv_file = open(csv_file_path)
        json_file = open(jsons_to_test_against[0])

        self.compare_json_to_csv(json_file, csv_file)


    def compare_json_to_csv(self, json_file, csv_file):

        # This unpacking is terrible and convoluted, but I don't want to spend any more time on it

        csv_reader = csv.reader(csv_file, delimiter=';', quotechar='|')
        
        csv_data = []
        for row in csv_reader:
            csv_data.append(row)
        
        csv_values = []

        for i in range(1, 3):
            for j in range(0, 4):
                csv_values.append(csv_data[i][j])

        json_values = []

        for item in json.loads(json_file.read()):
            for (key) in item:
                json_values.append(item[key])

        self.assertListEqual(csv_values, json_values)

if __name__ == "__main__":
    unittest.main()
