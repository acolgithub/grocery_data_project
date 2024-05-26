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

from obtain_data_foodbasics import FoodBasics
from obtain_data_independent import Independent
from obtain_data_loblaws import Loblaws
from obtain_data_longos import Longos
from obtain_data_metro import Metro
from obtain_data_nofrills import NoFrills
from obtain_data_valumart import Valumart

from grocery_store import GroceryStore


def scrape(grocery_store: str, grocery_item: str):

    # grocery store
    store = GroceryStore(grocery_store)

    content = ""
    
    # get content
    if grocery_store == "FoodBasics":
        content = store.selenium_scraper(grocery_item)

    else:
        content = store.html_session_scraper(grocery_item)

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


