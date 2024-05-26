import requests
from lxml import html

import re
import pandas as pd


import time
from collections import OrderedDict



class Longos():
        
    def __init__(self):

        self.url = "https://voila.ca/products/search?q="
        self.header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}

    def get_longos_deal_data(self, grocery_item: str):

        # form url with query
        url_query = self.url + grocery_item

        # store request
        r = ""

        # try to make request
        try:

            r = requests.get(url=url_query, headers=self.header)

        except UnboundLocalError as e:
            print(e)

            # close session
            r.close()

        finally:

            # get html
            h = html.fromstring(r.content)

            # close request
            r.close()

            # get brand, name, price, and unit of grocery item
            search_item_description = h.xpath("//*[@data-test='fop-title']")
            search_item_price = h.xpath("//*[@data-test='fop-price-per-unit']")

            # get descriptions
            search_item_description = [item.text for item in search_item_description]

            # get price using text_content due to new line characters
            search_item_price = [re.sub(r"[()]", "", price.text_content()) for price in search_item_price]
            
            # make columns
            columns = ["description", "price"]

            # make dataframe
            df = pd.DataFrame(data=[list(row) for row in zip(search_item_description, search_item_price)], columns=columns)

            return df

