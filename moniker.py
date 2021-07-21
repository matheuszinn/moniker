# Class to hold monikers related operations

import os
import glob
import json
import time

from typing import Optional

from tqdm import tqdm

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

SITE_URL = 'https://turmadamonicajovemedemais.blogspot.com/2019/04/blog-post.html'


class Moniker:

    def __init__(self, driver_options: webdriver.ChromeOptions, data_result_file: str = 'moniker_data.json', save: bool = False) -> None:
        self.driver_options = driver_options
        self.data_result_file = data_result_file
        self.moniker_data = None
        self.save = save

    def get_turma_da_moniker_data(self) -> Optional[list]:

        with webdriver.Chrome(executable_path='chromedriver.exe', options=self.driver_options, service_log_path='NUL') as driver:
            driver.get(SITE_URL)
            print(f'[*] Accessing: {SITE_URL}.')
            self.moniker_data = [[link_element.get_attribute('href')
                                  for link_element in ele.find_elements_by_tag_name('a')] for ele in driver.find_elements_by_xpath(
                '//*[@id="post-body-5703247609147775966"]')][0]

        if self.save:
            if glob.glob('./moniker_data.*'):
                print('Dados já obtidos em: moniker_data.json')
            else:
                with open(self.self.data_result_file, 'w+') as file:
                    json.dump(self.moniker_data, file, indent=2)

    # function tha execute the download
    def download_turma_da_monikers(self) -> None:

        self.get_turma_da_moniker_data()

        # To linux, change 'NUL' to 'dev/null'
        with webdriver.Chrome(executable_path='chromedriver.exe', options=self.driver_options, service_log_path='./chromedriver.log') as driver:

            # Initialize a progress bar
            with tqdm(total=len(self.moniker_data), desc='Stardownload') as download_bar:
                for link in self.moniker_data:

                    # Load the download page
                    driver.get(link)

                    # Check if there is a accept cookie button somewhere in the page
                    try:
                        cookie_button = driver.find_element_by_class_name(
                            'CookieAcceptance-accept')

                        if cookie_button:
                            # If it exists, click on it
                            cookie_button.click()
                    except NoSuchElementException:
                        pass

                    # get the download button
                    download_button = driver.find_element_by_id(
                        'downloadButton')
                    download_size = download_button.text
                    download_file_name = driver.find_element_by_class_name(
                        'filename').text

                    # change the progress bar description
                    download_bar.desc = f'{download_file_name} - {download_size.split(" ")[1]}'

                    # click the download button
                    download_button.click()

                    time.sleep(1)

                    # constantly check if there is a .crdownload file in the downloads page
                    while(True):
                        if not glob.glob('./**/*.crdownload'):
                            break

                    # Update the bar
                    download_bar.update(1)
