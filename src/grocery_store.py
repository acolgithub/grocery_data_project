import os
import re
import asyncio
import pandas as pd
from collections import OrderedDict

import lxml
from lxml import html

import aiohttp
from requests_html import AsyncHTMLSession
from playwright.async_api import async_playwright


class GroceryStore():

    def __init__(self, store_name: str) -> None:
        """
        Initialize object representing grocery store name and url.
        In addition, I have stored information regarding the header
        and options used when sending a request.

        Keyword arguments:
        store_name -- string containing the name of the store
        """

        # dictionary of grocery stores
        store_url_dictionary = {
            "FoodBasics": "https://www.foodbasics.ca/search?filter=",
            "Independent": "https://www.independentcitymarket.ca/search?search-bar=",
            "Loblaws": "https://www.loblaws.ca/search?search-bar=",
            "Longos": "https://voila.ca/products/search?q=",
            "Metro": "https://www.metro.ca/en/online-grocery/search?filter=",
            "NoFrills": "https://www.nofrills.ca/search?search-bar=",
            "Valumart": "https://www.valumart.ca/search?search-bar="
        }

        # class attributes
        self.store = store_name
        self.url = store_url_dictionary[store_name]
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
        }
        self.options = ["--window-size=1920,1080"]

    
    # function to save data obtained
    def save_data(self, df: pd.DataFrame) -> None:
        """
        Function to save retrieved data to file as html table.

        Keyword arguments:
        df -- dataframe containing grocery item price information
        """

        # convert to html dataframe
        html_df = df.to_html()

        # create results directory if it does not exist in working directory
        if not os.path.exists("results"):
            os.makedirs("results")

        # save in results with name corresponding to store and close
        text_file = open( "results/" + self.store + ".html", "w")
        text_file.write(html_df)
        text_file.close()


    # scraper used for Longos
    async def aiohttp_scraper(self, grocery_item: str) -> None:
        """
        Function that scrapes data using aiohttp and lxml.

        Keyword arguments:
        grocery_item -- desired item to get data on
        """

        # form url with query
        url_query = self.url + grocery_item

        # create http session
        async with aiohttp.ClientSession() as session:

            # make get request using session
            async with session.get(url_query) as response:

                # get text content
                response_text = await response.text()

                # get element tree
                tree = lxml.html.fromstring(response_text)

                # get description and price of grocery item
                search_item_description = tree.xpath("//*[@data-test='fop-title']")
                search_item_price = tree.xpath("//*[@data-test='fop-price-per-unit']")

                # get text of descriptions
                search_item_description = [item.text for item in search_item_description]

                # get price using text_content due to new line characters
                search_item_price = [re.sub(r"[()]", "", price.text_content()) for price in search_item_price]
                
                # make dataframe columns
                columns = ["description", "price"]

                # zip together information
                search_item_info = zip(search_item_description, search_item_price)

                # make dataframe
                df = pd.DataFrame(
                        data=[list(row) for row in search_item_info],
                        columns=columns
                    )

                # sort dataframe by brand contained in description
                df = df.sort_values(by=["description"], ignore_index=True)

                # save dataframe as html table
                self.save_data(df)
        

    # scraper used for Independent, Loblaws, No Frills, Valumart
    async def html_session_scraper(self, grocery_item: str) -> None:
        """
        Function using the requests-html and lxml in order to obtain
        data. This scraper is used for websites which require
        rendering JavaScript.

        Keyword arguments:
        grocery_item -- desired item to get data on
        """

        # form url with query
        url_query = self.url + grocery_item

        # get asynchronous session
        asession = AsyncHTMLSession()

        # store asynchronous session
        r = ""

        # try to go to url
        try:

            r = await asession.get(url_query)

            # render html and wait for html elements to appear
            await r.html.arender(sleep=10)

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
            search_item_eyebrow = h.xpath("//div[contains(@class, 'product-tile__eyebrow')]")

            # get brand, name, and price of grocery item
            search_item_brand = h.xpath("//span[contains(@class, 'product-name__item--brand')]")
            search_item_name = h.xpath("//span[contains(@class,'product-name__item--name')]")
            search_item_price = h.xpath("//*[@class='price selling-price-list__item__price selling-price-list__item__price--now-price'] | //*[@class='price selling-price-list__item__price selling-price-list__item__price--sale']")

            # get sponsor text but ignore 'new' and ignore repeat entries
            # note that we need to preserve the order of the entries
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

            # zip together information and enumerate
            search_item_info = enumerate(zip(search_item_brand, search_item_name, search_item_price))

            # make dataframe
            df = pd.DataFrame(
                    data=[list(row) for index, row in search_item_info if search_item_eyebrow[index] != "Sponsored"],
                    columns=columns
                )

            # sort dataframe
            df = df.sort_values(by=["brand"], ignore_index=True)

            # save dataframe as html table
            self.save_data(df)
            

   # scraper used for Food Basics, Metro
    async def playwright_scraper(self, grocery_item: str) -> None:
        """
        Function that scrapes data using playwright and lxml.
        This scraper is used for websites which require
        an interactive component.
        
        Keyword arguments:
        grocery_item -- desired item to get data on
        """

        # form url with query
        url_query = self.url + grocery_item

        async with async_playwright() as p:

            # get headless firefox browser
            browser = await p.firefox.launch(headless=True, args=self.options)

            # add user agent
            context = await browser.new_context(user_agent=self.header["user-agent"])

            # get new page
            page = await context.new_page()

            # search query
            await page.goto(url_query)

            # locate privacy button and click
            await page.locator('xpath=//button[@id="onetrust-reject-all-handler"]').click()

            # get page content
            page_content = await page.content()

            # convert page content to html
            tree = lxml.html.fromstring(page_content)

            # get brand, description, price, and unit of grocery item
            search_item_brand = tree.xpath("//span[@class='head__brand']")
            search_item_description = tree.xpath("//*[@class='head__title']")
            search_item_unit = tree.xpath("//*[@class='head__unit-details']")
            search_item_price = tree.xpath("//div[@data-main-price]")

            # get formatted brand name
            search_item_brand = [re.sub(r"\n", "", brand.text) for brand in search_item_brand]

            # get description text
            search_item_description = [description.text for description in search_item_description]

            # get item unit
            search_item_unit = [unit.text for unit in search_item_unit]

            # extract price
            search_item_price = [price.get("data-main-price") for price in search_item_price]

            # make columns   
            columns = ["brand", "description", "unit", "price"]

            # zip together information
            search_item_info = zip(search_item_brand, search_item_description, search_item_unit, search_item_price)

            # make dataframe
            df = pd.DataFrame(
                    data=[list(row) for row in search_item_info],
                    columns=columns
                )

            # sort dataframe
            df = df.sort_values(by=["brand"], ignore_index=True)

            # save dataframe as html table
            self.save_data(df)


    # get appropriate scraper
    async def get_scraper(self, grocery_item: str) -> None:
        """
        Function that returns the appropriate data scraper for a given
        store.

        Keyword arguments:
        grocery_item -- desired item to get data on
        """

        # use aiohttp_scraper for Longos
        if self.store == "Longos":

            await self.aiohttp_scraper(grocery_item)

        # use html_session_scraper for Independent, Loblaws, No Frills, and Valumart
        elif self.store in ["Independent", "Loblaws", "NoFrills", "Valumart"]:

            await self.html_session_scraper(grocery_item)

        # use playwright_scraper for Food Basics and Metro
        elif self.store in ["FoodBasics", "Metro"]:

            await self.playwright_scraper(grocery_item)
        
        # all other inputs result in error
        else:

            print("Error, no matching store.")

