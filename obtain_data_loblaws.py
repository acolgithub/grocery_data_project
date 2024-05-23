import requests
from lxml import html

import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from collections import OrderedDict


from requests_html import HTMLSession



class Loblaws():
        
    def __init__(self):

        self.url = "https://www.loblaws.ca"
        self.header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}
        self.options = FirefoxOptions()

        # run headless
        self.options.add_argument("--headless")

        # adjust window size
        self.options.add_argument("window-size=1920,1080")


    def get_loblaws_data(self, grocery_item: str):


        # form url with query
        url_query = self.url + "/search?search-bar=" + grocery_item

        # get session object
        session = HTMLSession()

        # try to go to url
        try:

            r = session.get(url_query)

            # render html and wait for html elements to appear
            r.html.render(sleep=3)

        except UnboundLocalError as e:
            print(e)

            # close session
            r.close()

        finally:

            # get html
            h = r.html

            # close session
            r.close()

            # determine which items are sponspored
            search_item_eyebrow = h.xpath("//*[@class='product-tile__eyebrow']")

            # get brand, name, price, and unit of grocery item
            search_item_brand = h.xpath("//*[@class='product-name__item product-name__item--brand']")
            search_item_name = h.xpath("//*[@class='product-name__item product-name__item--name']")
            search_item_price = h.xpath("//*[@class='price selling-price-list__item__price selling-price-list__item__price--now-price'] | //*[@class='price selling-price-list__item__price selling-price-list__item__price--sale']")

            # # get sponsor text but ignore 'new' and ignore repeat entries
            search_item_eyebrow = list(OrderedDict.fromkeys([(brow.attrs["data-testid"], re.sub(re.escape("New"), "", brow.text)) for brow in search_item_eyebrow]))
            search_item_eyebrow = [tup[1] for tup in search_item_eyebrow]

            # get brand text
            search_item_brand = [brand.text for brand in search_item_brand]

            # get item text
            search_item_name = [name.text for name in search_item_name]

            # format price
            price_regex = r"(\.\d{2})(.*)"
            search_item_price = [re.sub(price_regex, r'\1 \2', price.text) for price in search_item_price]

            # make columns   
            columns = ["brand", "name", "price"]

            # make dataframe
            df = pd.DataFrame(data=[list(row) for index, row in enumerate(zip(search_item_brand, search_item_name, search_item_price)) if search_item_eyebrow[index] != "Sponsored"], columns=columns)

            return df.sort_values(by=["brand", "price"], ignore_index=True)
        



loblaws = Loblaws()

t0 = time.time()
print(loblaws.get_loblaws_data("milk"))
print(time.time() - t0)




