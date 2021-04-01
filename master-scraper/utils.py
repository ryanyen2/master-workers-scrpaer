import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import random
import const

# add on your own SSL certificate or using this unsafe certificate
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def init_driver():
    chromedriver_path = chromedriver_autoinstaller.install()
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    if const.APP_ENV != 'local':
        options.add_argument('--headless')

    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options, executable_path=chromedriver_path)
    driver.set_page_load_timeout(100)
    return driver


def fetch_search_page(driver, from_account, start_date):
    from_account = "(from%3A" + from_account + ")%20" if from_account is not None else ""
    start_date = "since%3A" + start_date + "%20"

    # construct the path (using twitter as example
    path = 'https://twitter.com/search?q=' + from_account + start_date + "%20-filter%3Areplies" + '&src=typed_query'

    driver.get(path)
    sleep(random.uniform(3.3, 8.3))


def check_new_update(driver):
    sleep(random.uniform(3.5, 7.9))
    return True if driver.find_elements_by_xpath('') else False
