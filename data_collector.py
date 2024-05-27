import re
import random
import pandas as pd
from itertools import repeat

import asyncio

import time
from collections import OrderedDict

import requests

from requests_html import HTMLSession
from lxml import html

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from grocery_store import GroceryStore


async def scrape(grocery_store: str, grocery_item: str):

    # add random delay
    time.sleep(random.uniform(0,2))

    # grocery store
    store = GroceryStore(grocery_store)
    
    # get content
    content = store.get_scraper(grocery_item)

    # print content
    print(content)
    print(grocery_store)

async def main():

    t0 = time.time()

    grocery_item = "milk"

    stores = [
        "FoodBasics", "Independent", "Loblaws", "Longos", "Metro", "NoFrills", "Valumart"
    ]

    tasks = [asyncio.create_task(scrape(store, grocery_item)) for store in stores]

    await asyncio.gather(*tasks)

    print(time.time() - t0)


if __name__ == "__main__":

    asyncio.run(main())


