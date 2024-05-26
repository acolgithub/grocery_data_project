import re
import pandas as pd
from itertools import repeat
from multiprocessing import Process, Pool

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
    content = store.get_scraper("milk")

    # print content
    print(content)


if __name__ == "__main__":

    t0 = time.time()

    grocery_item = "milk"

    jobs = [
        "FoodBasics", "Independent", "Loblaws", "Longos", "Metro", "NoFrills", "Valumart"
    ]

    with Pool(processes=len(jobs)) as pool:
        
        # get result of scraping
        pool.starmap(scrape, zip(jobs, repeat(grocery_item)))


    print(time.time() - t0)


