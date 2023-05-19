from os import environ as env, mkdir
import json

from dotenv import load_dotenv
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.common.by import By

def get_headline(url, driver):
    driver.get(url)
    return driver.find_element(By.TAG_NAME,'h1').text


def handler(event, context):
    firefox_options = Options()
    firefox_options.add_argument("-headless")
    firefox_options.binary_location = '/opt/firefox/113.0/firefox/firefox'
    tmp_dir = '/tmp/ff' 
    mkdir(tmp_dir)
    ff_profile = FirefoxProfile(profile_directory=tmp_dir)
    driver = Firefox(firefox_profile=ff_profile,
                     executable_path='/opt/geckodriver/0.33.0/geckodriver',
                     options=firefox_options,
                     service_log_path='/tmp/geckodriver.log')

    # Proof!
    url = "https://www.bbc.co.uk/news/world-europe-45753455"
    headline = get_headline(url, driver)

    driver.close()

    return headline

if __name__ == "__main__":
    load_dotenv()
    print(env.get("EXAMPLE"))
    print(handler(None, None))