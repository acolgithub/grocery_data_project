import requests
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions






# get relevant stories
def get_loblaws_deal_data(regex_search_words: list[str]):

    # get Firefox options
    # options = FirefoxOptions()

    # set headless mode
    # options.add_argument("--headless")

    # get url
    url = "https://www.loblaws.ca/"
    header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}

    # form url with query
    url_query = url #+ "/site-search/?query=" + word

    # get profile
    driver = webdriver.Firefox()

    # go to url
    driver.get(url)

    # # go to website
    # root_div = driver.find_element(By.XPATH, "//div[@id='root']")

    # # get tag
    # print(root_div.find_element(By.XPATH, "//div[@id='site-layout']"))

    # driver.quit()



get_loblaws_deal_data(["milk"])