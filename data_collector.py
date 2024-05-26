from multiprocessing import Process
import re
import pandas as pd

import time
from collections import OrderedDict

from requests_html import HTMLSession
from lxml import html

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from grocery_store import GroceryStore


def scrape(grocery_store: str, grocery_item: str):

    # grocery store
    store = GroceryStore(grocery_store)
    
    # get content
    content = store.get_scraper( "milk")

    # print content
    print(content)


if __name__ == "__main__":

    t0 = time.time()
    p1 = Process(target=scrape, args=("FoodBasics", "milk"))
    p1.start()
    p2 = Process(target=scrape, args=("Loblaws", "milk"))
    p2.start()
    p1.join()
    p2.join()
    print(time.time() - t0)


