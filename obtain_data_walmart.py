from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.action_chains import ActionChains

from requests_html import HTMLSession


import time
from collections import OrderedDict


from requests_html import HTMLSession



class Walmart():

    def __init__(self):

        self.url = "https://www.walmart.ca/en"
        self.header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}
        self.options = FirefoxOptions()

        # run headless
        self.options.add_argument("--headless")

        # adjust window size
        self.options.add_argument("window-size=1920,1080")


    def get_walmart_deal_data(self, grocery_item: str):

        # form url with query
        url_query = self.url + "/search?q=" + grocery_item

        # get driver
        driver = webdriver.Firefox(options=self.options)

        # go to url
        driver.get(url_query)

        # try to make request
        try:

            # wait until privacy element is visible
            WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//h2[@class="tc relative"]')))

            # click not to accept cookies
            privacy_button = driver.find_element(By.XPATH, "//button[@aria-label='closeDialogLabel']")
            privacy_button.click()

            # wait until desired elements load
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='list-view']"))
            )
        
        except requests.exceptions.HTTPError as e:

            # catastrophic error
            raise SystemExit(e)
        
        finally:

            # get description and price
            search_item_price = element.find_elements(By.XPATH, "//*[@data-automation-id='product-price']")
            search_item_description = element.find_elements(By.XPATH, "//*[@data-automation-id='product-title']")

            search_item_price = [price.text for price in search_item_price]
            search_item_description = [description.text for description in search_item_description]

            print(search_item_price)
            print(search_item_description)
            
            driver.quit()





    def get_walmart_deal_data2(self, grocery_item: str):

        # form url with query
        url_query = self.url + "/search?q=" + grocery_item

        # get session object
        session = HTMLSession()

        # try to make request
        try:

            r = session.get(url=url_query, headers=self.header)

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

            print(h)

            # # get brand, name, price, and unit of grocery item
            # search_item_description = h.xpath("//*[@data-automation-id='product-title']")
            # search_item_price = h.xpath("//*[@data-automation-id='product-price']")

            # print(search_item_description)

            



walmart = Walmart()

t0 = time.time()
walmart.get_walmart_deal_data2("milk")
print(time.time() - t0)


