import os
import glob
import json
import time

from typing import Optional

from tqdm import tqdm

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

if not os.path.isdir('./downloads'):
    os.mkdir('downloads')

SITE_URL = 'https://turmadamonicajovemedemais.blogspot.com/2019/04/blog-post.html'
DATA_RESULT_FILE = 'moniker_data.json'


# Set the options for the chromedriver
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory': os.getcwd() + '\\downloads\\'}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.headless = True
chrome_options.add_argument('--hide-scrollbars')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--log-level=3')

TEXT = '''

███╗   ███╗ ██████╗ ███╗   ██╗██╗██╗  ██╗███████╗██████╗ 
████╗ ████║██╔═══██╗████╗  ██║██║██║ ██╔╝██╔════╝██╔══██╗
██╔████╔██║██║   ██║██╔██╗ ██║██║█████╔╝ █████╗  ██████╔╝
██║╚██╔╝██║██║   ██║██║╚██╗██║██║██╔═██╗ ██╔══╝  ██╔══██╗
██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║██║  ██╗███████╗██║  ██║
╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                         
                                by Matheuszinn

'''

# function that seach the download links and store them by default
# maybe used with the flag 'list' to return a list containing all the download links


def get_turma_da_moniker_data(mode: str = 'save') -> Optional[list]:

    data = None

    with webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options, service_log_path='NUL') as driver:
        driver.get(SITE_URL)
        print(f'[*] Accessing: {SITE_URL}.')
        data = [[link_element.get_attribute('href')
                 for link_element in ele.find_elements_by_tag_name('a')] for ele in driver.find_elements_by_xpath(
            '//*[@id="post-body-5703247609147775966"]')][0]

    if mode == 'save':
        if glob.glob('./moniker_data.*'):
            print('Dados já obtidos em: moniker_data.json')
        else:
            with open(DATA_RESULT_FILE, 'w+') as file:
                json.dump(data, file, indent=2)

    if mode == 'list':
        return data


# function tha execute the download

def download_turma_da_monikers() -> None:

    moniker_data = get_turma_da_moniker_data(mode='list')

    # To linux, change 'NUL' to 'dev/null'
    with webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options, service_log_path='./chromedriver.log') as driver:

        # Initialize a progress bar
        with tqdm(total=len(moniker_data), desc='Stardownload') as download_bar:
            for link in moniker_data:

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

                #Update the bar
                download_bar.update(1)


print(TEXT)
download_turma_da_monikers()
