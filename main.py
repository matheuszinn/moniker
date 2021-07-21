from moniker import Moniker
from selenium import webdriver

import os

from utils import file_renamer

if not os.path.isdir('./downloads'):
    os.mkdir('downloads')

DOWNLOAD_FOLDER = os.getcwd() + '\\downloads\\'

# Set the options for the chromedriver
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory': DOWNLOAD_FOLDER}
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

print(TEXT)
Moniker(driver_options=chrome_options).download_turma_da_monikers()
file_renamer(DOWNLOAD_FOLDER)
