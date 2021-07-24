from moniker import Moniker
from selenium import webdriver

import os

from utils import file_renamer
from utils import pdf2cbz

if not os.path.isdir('./downloads'):
    os.mkdir('downloads')

if not os.path.isdir("./cbz'ed_files"):
    os.mkdir("cbz'ed_files")

DOWNLOAD_FOLDER = os.getcwd() + '/downloads/'
CBZ_FOLDER = os.getcwd() + "/cbz'ed_files/"

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

## Download the files
Moniker(driver_options=chrome_options).download_turma_da_monikers()

# Rename the files
file_renamer(DOWNLOAD_FOLDER)

# Turn the pdf files into cbz
pdf2cbz(DOWNLOAD_FOLDER, CBZ_FOLDER)
