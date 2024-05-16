from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from selenium import webdriver




# get relevant stories
def get_reuters_data(regex_search_words: list[str]):

    # get url
    url = "https://www.reuters.com"
    header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}


    # iterate over search words
    for word in regex_search_words:

        # form url with query
        url_query = url + "/site-search/?query=" + word

        # # get firefox options
        # firefox_options = Options()

        # get profile
        driver = webdriver.Firefox()

        # go to website
        driver.get(url_query)

        #
        descriptions = driver.find_element(
            "xpath",
            "//span[@class='text__text__1FZLe text__dark-grey__3Ml43 text__medium__1kbOh text__heading_6__1qUJ5 heading__base__2T28j heading__heading_6__RtD9P']"
        )

        print(descriptions)

        driver.close()






# search terms
search_terms = ["internet scam", "cyber crime", "phishing", "fraudster", "data breach"]

# convert to search words
search_words = ["+".join(term.split()) for term in search_terms]

# regex search words
regex_search_words = [r"\b" + re.escape(word) + r"\b" for word in search_words]

get_reuters_data([r"hackers"])