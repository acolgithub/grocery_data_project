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

from grocery_store import GroceryStore


# function to srape data
async def scrape(grocery_store: str, grocery_item: str) -> None:
    """
    Function that collects data about an item from a specified grocery store.

    Keyword arguments:
    grocery_store -- name of grocery store of interest
    grocery_item -- desired item to get data on
    """

    # initialize grocery store object
    store = GroceryStore(grocery_store)
    
    # get data about desired item from specified store
    await store.get_scraper(grocery_item)


# collect data from each grocery store regarding desired item
async def main() -> None:
    """
    Main function which requests desired grocery item and collects
    data from a number of grocery stores.
    """

    # prompt user for grocery item
    print("Please input a grocery item:")

    # item to search
    grocery_item = input()

    # grocery stores to search
    stores = [
        "FoodBasics", "Independent", "Loblaws", "Longos", "Metro", "NoFrills", "Valumart"
    ]

    # create coroutines
    async with asyncio.TaskGroup() as tg:

        for store in stores:

            tg.create_task(scrape(store, grocery_item))


if __name__ == "__main__":

    # get event loop in the current thread
    loop = asyncio.get_event_loop()

    # run main function to acquire data
    loop.run_until_complete(main())
